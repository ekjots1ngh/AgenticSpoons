(* JSON-RPC server for Python integration *)
open Core
open Volatility_engine

let handle_request json_str =
  try
    let json = Yojson.Safe.from_string json_str in
    let open Yojson.Safe.Util in
    
    let method_name = json |> member "method" |> to_string in
    let params = json |> member "params" in
    
    match method_name with
    | "calculate_volatility" ->
        let data = params |> member "data" |> to_list |> List.map ~f:(fun item ->
          let timestamp = item |> member "timestamp" |> to_float in
          let open_ = item |> member "open" |> to_float in
          let high = item |> member "high" |> to_float in
          let low = item |> member "low" |> to_float in
          let close = item |> member "close" |> to_float in
          let volume = item |> member "volume" |> to_float in
          Volatility.OHLCV.{ timestamp; open_; high; low; close; volume }
        ) in
        
        let data_array = Array.of_list data in
        let metrics = Volatility.HistoricalVol.calculate_all data_array in
        
        let response = Volatility.VolatilityMetrics.yojson_of_t metrics in
        Yojson.Safe.to_string response
    
    | "calculate_greeks" ->
        let s = params |> member "spot" |> to_float in
        let k = params |> member "strike" |> to_float in
        let t = params |> member "maturity" |> to_float in
        let r = params |> member "risk_free_rate" |> to_float in
        let sigma = params |> member "volatility" |> to_float in
        let option_type = 
          match params |> member "option_type" |> to_string with
          | "call" -> `Call
          | "put" -> `Put
          | _ -> `Call
        in
        
        let greeks = Volatility.BlackScholes.calculate_greeks ~s ~k ~t ~r ~sigma ~option_type in
        let response = Volatility.BlackScholes.yojson_of_greeks greeks in
        Yojson.Safe.to_string response
    
    | "fit_garch" ->
        let returns = params |> member "returns" |> to_list |> List.map ~f:to_float |> Array.of_list in
        let result = Volatility.GARCH.fit returns in
        let response = Volatility.GARCH.yojson_of_result result in
        Yojson.Safe.to_string response
    
    | "monte_carlo_option" ->
        let s0 = params |> member "spot" |> to_float in
        let k = params |> member "strike" |> to_float in
        let t = params |> member "maturity" |> to_float in
        let r = params |> member "risk_free_rate" |> to_float in
        let sigma = params |> member "volatility" |> to_float in
        let n_paths = params |> member "n_paths" |> to_int in
        let option_type = 
          match params |> member "option_type" |> to_string with
          | "call" -> `Call
          | "put" -> `Put
          | _ -> `Call
        in
        
        let (price, std_error) = Volatility.MonteCarlo.price_european_option 
          ~s0 ~k ~t ~r ~sigma ~option_type ~n_paths in
        
        let response = `Assoc [
          ("price", `Float price);
          ("std_error", `Float std_error);
        ] in
        Yojson.Safe.to_string response
    
    | _ ->
        Yojson.Safe.to_string (`Assoc [("error", `String "Unknown method")])
  
  with e ->
    Yojson.Safe.to_string (`Assoc [("error", `String (Exn.to_string e))])

let () =
  (* Read from stdin, write to stdout *)
  In_channel.iter_lines In_channel.stdin ~f:(fun line ->
    let response = handle_request line in
    Out_channel.output_string Out_channel.stdout (response ^ "\n");
    Out_channel.flush Out_channel.stdout
  )
