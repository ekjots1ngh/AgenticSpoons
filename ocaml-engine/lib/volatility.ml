(* AgentSpoons OCaml Volatility Engine *)
open Core
open Owl

module VolatilityMetrics = struct
  type t = {
    close_to_close: float;
    parkinson: float;
    garman_klass: float;
    rogers_satchell: float;
    yang_zhang: float;
  } [@@deriving sexp, yojson]
end

module OHLCV = struct
  type t = {
    timestamp: float;
    open_: float;
    high: float;
    low: float;
    close: float;
    volume: float;
  } [@@deriving sexp, yojson]
  
  let to_array data =
    Array.of_list data
end

(* Historical Volatility Calculations *)
module HistoricalVol = struct
  
  let annualization_factor = sqrt 252.0
  
  (* Close-to-Close Volatility *)
  let close_to_close (prices: float array) : float =
    let n = Array.length prices in
    if n < 2 then 0.0
    else
      let returns = Array.init (n - 1) (fun i ->
        log (prices.(i + 1) /. prices.(i))
      ) in
      let mean_return = Stats.mean returns in
      let variance = Stats.var ~mean:mean_return returns in
      sqrt variance *. annualization_factor
  
  (* Parkinson Volatility - uses high-low range *)
  let parkinson (data: OHLCV.t array) : float =
    let n = Array.length data in
    if n < 2 then 0.0
    else
      let hl_ratios = Array.map data ~f:(fun candle ->
        let hl = log (candle.high /. candle.low) in
        hl *. hl
      ) in
      let factor = 1.0 /. (4.0 *. log 2.0) in
      let mean_hl = Stats.mean hl_ratios in
      sqrt (252.0 *. factor *. mean_hl)
  
  (* Garman-Klass Volatility - best OHLC estimator *)
  let garman_klass (data: OHLCV.t array) : float =
    let n = Array.length data in
    if n < 2 then 0.0
    else
      let gk_components = Array.map data ~f:(fun candle ->
        let hl = log (candle.high /. candle.low) in
        let co = log (candle.close /. candle.open_) in
        0.5 *. hl *. hl -. (2.0 *. log 2.0 -. 1.0) *. co *. co
      ) in
      let mean_gk = Stats.mean gk_components in
      sqrt (252.0 *. mean_gk)
  
  (* Rogers-Satchell Volatility - allows for drift *)
  let rogers_satchell (data: OHLCV.t array) : float =
    let n = Array.length data in
    if n < 2 then 0.0
    else
      let rs_components = Array.map data ~f:(fun candle ->
        let hc = log (candle.high /. candle.close) in
        let ho = log (candle.high /. candle.open_) in
        let lc = log (candle.low /. candle.close) in
        let lo = log (candle.low /. candle.open_) in
        hc *. ho +. lc *. lo
      ) in
      let mean_rs = Stats.mean rs_components in
      sqrt (252.0 *. mean_rs)
  
  (* Yang-Zhang Volatility - combines multiple estimators *)
  let yang_zhang (data: OHLCV.t array) : float =
    let n = Array.length data in
    if n < 3 then 0.0
    else
      (* Overnight volatility *)
      let overnight = Array.init (n - 1) (fun i ->
        log (data.(i + 1).open_ /. data.(i).close)
      ) in
      let overnight_var = Stats.var overnight in
      
      (* Open-to-close (Rogers-Satchell) *)
      let rs = rogers_satchell data in
      let rs_var = rs *. rs /. 252.0 in
      
      (* Close-to-close *)
      let closes = Array.map data ~f:(fun c -> c.close) in
      let cc = close_to_close closes in
      let cc_var = cc *. cc /. 252.0 in
      
      (* Yang-Zhang combination *)
      let k = 0.34 /. (1.34 +. (float_of_int (n + 1)) /. (float_of_int (n - 1))) in
      let yz_var = overnight_var +. k *. cc_var +. (1.0 -. k) *. rs_var in
      
      sqrt (252.0 *. yz_var)
  
  (* Calculate all metrics at once *)
  let calculate_all (data: OHLCV.t array) : VolatilityMetrics.t =
    let closes = Array.map data ~f:(fun c -> c.close) in
    {
      close_to_close = close_to_close closes;
      parkinson = parkinson data;
      garman_klass = garman_klass data;
      rogers_satchell = rogers_satchell data;
      yang_zhang = yang_zhang data;
    }
end

(* Black-Scholes Model with automatic differentiation *)
module BlackScholes = struct
  
  type greeks = {
    delta: float;
    gamma: float;
    vega: float;
    theta: float;
    rho: float;
  } [@@deriving sexp, yojson]
  
  let normal_cdf x =
    (* Standard normal CDF using error function *)
    0.5 *. (1.0 +. erf (x /. sqrt 2.0))
  
  let normal_pdf x =
    (* Standard normal PDF *)
    (1.0 /. sqrt (2.0 *. Float.pi)) *. exp (-0.5 *. x *. x)
  
  let d1 ~s ~k ~t ~r ~sigma =
    (log (s /. k) +. (r +. 0.5 *. sigma *. sigma) *. t) /. (sigma *. sqrt t)
  
  let d2 ~s ~k ~t ~r ~sigma =
    d1 ~s ~k ~t ~r ~sigma -. sigma *. sqrt t
  
  let call_price ~s ~k ~t ~r ~sigma =
    let d1_val = d1 ~s ~k ~t ~r ~sigma in
    let d2_val = d2 ~s ~k ~t ~r ~sigma in
    s *. normal_cdf d1_val -. k *. exp (-.r *. t) *. normal_cdf d2_val
  
  let put_price ~s ~k ~t ~r ~sigma =
    let d1_val = d1 ~s ~k ~t ~r ~sigma in
    let d2_val = d2 ~s ~k ~t ~r ~sigma in
    k *. exp (-.r *. t) *. normal_cdf (-.d2_val) -. s *. normal_cdf (-.d1_val)
  
  (* Greeks calculations *)
  let calculate_greeks ~s ~k ~t ~r ~sigma ~option_type =
    let d1_val = d1 ~s ~k ~t ~r ~sigma in
    let d2_val = d2 ~s ~k ~t ~r ~sigma in
    
    let delta = match option_type with
      | `Call -> normal_cdf d1_val
      | `Put -> normal_cdf d1_val -. 1.0
    in
    
    let gamma = normal_pdf d1_val /. (s *. sigma *. sqrt t) in
    
    let vega = s *. normal_pdf d1_val *. sqrt t in
    
    let theta = match option_type with
      | `Call ->
          -.(s *. normal_pdf d1_val *. sigma) /. (2.0 *. sqrt t)
          -. r *. k *. exp (-.r *. t) *. normal_cdf d2_val
      | `Put ->
          -.(s *. normal_pdf d1_val *. sigma) /. (2.0 *. sqrt t)
          +. r *. k *. exp (-.r *. t) *. normal_cdf (-.d2_val)
    in
    
    let rho = match option_type with
      | `Call -> k *. t *. exp (-.r *. t) *. normal_cdf d2_val
      | `Put -> -.k *. t *. exp (-.r *. t) *. normal_cdf (-.d2_val)
    in
    
    { delta; gamma; vega; theta = theta /. 365.0; rho = rho /. 100.0 }
  
  (* Newton-Raphson implied volatility solver *)
  let implied_volatility ~option_price ~s ~k ~t ~r ~option_type
      ?(initial_guess=0.3) ?(max_iterations=100) ?(tolerance=1e-6) () =
    
    let rec newton_raphson sigma iteration =
      if iteration >= max_iterations then sigma
      else
        let price = match option_type with
          | `Call -> call_price ~s ~k ~t ~r ~sigma
          | `Put -> put_price ~s ~k ~t ~r ~sigma
        in
        
        let vega = s *. normal_pdf (d1 ~s ~k ~t ~r ~sigma) *. sqrt t in
        
        if abs_float vega < 1e-10 then sigma
        else
          let diff = option_price -. price in
          if abs_float diff < tolerance then sigma
          else
            let new_sigma = sigma +. diff /. vega in
            let bounded_sigma = Float.max 0.001 (Float.min 5.0 new_sigma) in
            newton_raphson bounded_sigma (iteration + 1)
    in
    
    newton_raphson initial_guess 0
end

(* Monte Carlo Simulation Engine *)
module MonteCarlo = struct
  
  (* Geometric Brownian Motion simulation *)
  let simulate_gbm ~s0 ~mu ~sigma ~dt ~n_steps ~n_paths =
    let paths = Mat.empty n_paths n_steps in
    
    (* Initialize first column with S0 *)
    Mat.set_slice [[];[0]] paths (Mat.of_array [|s0|] n_paths 1);
    
    (* Generate random walks *)
    for t = 1 to n_steps - 1 do
      for path = 0 to n_paths - 1 do
        let s_prev = Mat.get paths path (t - 1) in
        let z = Stats.Rnd.gaussian ~mu:0.0 ~sigma:1.0 in
        let drift = (mu -. 0.5 *. sigma *. sigma) *. dt in
        let diffusion = sigma *. sqrt dt *. z in
        let s_next = s_prev *. exp (drift +. diffusion) in
        Mat.set paths path t s_next
      done
    done;
    
    paths
  
  (* Price European option via Monte Carlo *)
  let price_european_option ~s0 ~k ~t ~r ~sigma ~option_type ~n_paths =
    let final_prices = Array.init n_paths (fun _ ->
      let z = Stats.Rnd.gaussian ~mu:0.0 ~sigma:1.0 in
      let drift = (r -. 0.5 *. sigma *. sigma) *. t in
      let diffusion = sigma *. sqrt t *. z in
      s0 *. exp (drift +. diffusion)
    ) in
    
    let payoffs = Array.map final_prices ~f:(fun s_t ->
      match option_type with
      | `Call -> Float.max 0.0 (s_t -. k)
      | `Put -> Float.max 0.0 (k -. s_t)
    ) in
    
    let mean_payoff = Stats.mean payoffs in
    let std_error = Stats.std payoffs /. sqrt (float_of_int n_paths) in
    
    (mean_payoff *. exp (-.r *. t), std_error *. exp (-.r *. t))
  
  (* Variance reduction: Antithetic variates *)
  let price_with_antithetic ~s0 ~k ~t ~r ~sigma ~option_type ~n_paths =
    let half_paths = n_paths / 2 in
    
    let payoffs = Array.init half_paths (fun _ ->
      let z = Stats.Rnd.gaussian ~mu:0.0 ~sigma:1.0 in
      let drift = (r -. 0.5 *. sigma *. sigma) *. t in
      let diffusion = sigma *. sqrt t in
      
      (* Positive path *)
      let s1 = s0 *. exp (drift +. diffusion *. z) in
      let payoff1 = match option_type with
        | `Call -> Float.max 0.0 (s1 -. k)
        | `Put -> Float.max 0.0 (k -. s1)
      in
      
      (* Antithetic path *)
      let s2 = s0 *. exp (drift -. diffusion *. z) in
      let payoff2 = match option_type with
        | `Call -> Float.max 0.0 (s2 -. k)
        | `Put -> Float.max 0.0 (k -. s2)
      in
      
      (payoff1 +. payoff2) /. 2.0
    ) in
    
    let mean_payoff = Stats.mean payoffs in
    mean_payoff *. exp (-.r *. t)
end

(* GARCH(1,1) Model - Maximum Likelihood Estimation *)
module GARCH = struct
  
  type params = {
    omega: float;
    alpha: float;
    beta: float;
  } [@@deriving sexp, yojson]
  
  type result = {
    params: params;
    conditional_variance: float array;
    log_likelihood: float;
  } [@@deriving sexp, yojson]
  
  (* Calculate conditional variance given parameters *)
  let conditional_variance ~returns ~omega ~alpha ~beta =
    let n = Array.length returns in
    let variance = Array.create ~len:n 0.0 in
    
    (* Initial variance = sample variance *)
    variance.(0) <- Stats.var returns;
    
    (* GARCH recursion: σ²_t = ω + α*ε²_(t-1) + β*σ²_(t-1) *)
    for t = 1 to n - 1 do
      let eps_sq = returns.(t - 1) *. returns.(t - 1) in
      variance.(t) <- omega +. alpha *. eps_sq +. beta *. variance.(t - 1);
    done;
    
    variance
  
  (* Log-likelihood function *)
  let log_likelihood ~returns ~omega ~alpha ~beta =
    let variance = conditional_variance ~returns ~omega ~alpha ~beta in
    let n = Array.length returns in
    
    let ll = ref 0.0 in
    for t = 0 to n - 1 do
      if variance.(t) > 0.0 then
        ll := !ll -. 0.5 *. (log (2.0 *. Float.pi) +. log variance.(t) 
                            +. returns.(t) *. returns.(t) /. variance.(t))
    done;
    !ll
  
  (* Simplified MLE - using grid search (for hackathon demo) *)
  (* In production, use proper optimization *)
  let fit (returns: float array) : result =
    let best_params = ref { omega = 0.0001; alpha = 0.05; beta = 0.90 } in
    let best_ll = ref Float.neg_infinity in
    
    (* Grid search over parameter space *)
    let omega_range = [0.00001; 0.0001; 0.001] in
    let alpha_range = [0.03; 0.05; 0.08; 0.10] in
    let beta_range = [0.85; 0.90; 0.93; 0.95] in
    
    List.iter omega_range ~f:(fun omega ->
      List.iter alpha_range ~f:(fun alpha ->
        List.iter beta_range ~f:(fun beta ->
          (* Ensure stationarity: alpha + beta < 1 *)
          if alpha +. beta < 0.999 then
            let ll = log_likelihood ~returns ~omega ~alpha ~beta in
            if ll > !best_ll then begin
              best_ll := ll;
              best_params := { omega; alpha; beta }
            end
        )
      )
    );
    
    let variance = conditional_variance ~returns 
                     ~omega:(!best_params).omega
                     ~alpha:(!best_params).alpha
                     ~beta:(!best_params).beta in
    
    { params = !best_params; conditional_variance = variance; log_likelihood = !best_ll }
  
  (* Forecast volatility *)
  let forecast ~result ~horizon =
    let { omega; alpha; beta } = result.params in
    let n = Array.length result.conditional_variance in
    let last_variance = result.conditional_variance.(n - 1) in
    
    (* Multi-step forecast *)
    let forecasts = Array.create ~len:horizon 0.0 in
    forecasts.(0) <- omega +. (alpha +. beta) *. last_variance;
    
    for h = 1 to horizon - 1 do
      let persistence = Float.pow (alpha +. beta) (float_of_int h) in
      let long_run_var = omega /. (1.0 -. alpha -. beta) in
      forecasts.(h) <- long_run_var *. (1.0 -. persistence) +. persistence *. last_variance;
    done;
    
    (* Return annualized volatility *)
    Array.map forecasts ~f:(fun var -> sqrt (252.0 *. var))
end
