# AgentSpoons Architecture

```mermaid
graph TD
    A[User/DApp] -->|Query| B[REST API]
    B --> C{SpoonOS Coordinator}
    
    C -->|Task 1| D[Market Data Collector]
    C -->|Task 2| E[Volatility Calculator]
    C -->|Task 3| F[Implied Vol Engine]
    C -->|Task 4| G[GARCH Forecaster]
    C -->|Task 5| H[Arbitrage Detector]
    C -->|Task 6| I[Neo Publisher]
    
    D -->|Price Data| J[(Redis Cache)]
    E -->|7 Models| K[Parkinson<br/>Garman-Klass<br/>Rogers-Satchell<br/>Yang-Zhang<br/>Realized Kernel<br/>Bipower Var<br/>Close-to-Close]
    
    F -->|Options Data| L[Black-Scholes<br/>C++ Engine]
    G -->|Time Series| M[GARCH Model<br/>OCaml Engine]
    H -->|Signals| N[ML Models<br/>LSTM + XGBoost]
    
    I -->|Publish| O[Neo N3 Smart Contract]
    O -->|Store| P[(Neo Blockchain)]
    
    J -.->|Feed| E
    J -.->|Feed| F
    
    style C fill:#2563eb,stroke:#1e40af,color:#fff
    style I fill:#10b981,stroke:#059669,color:#fff
    style O fill:#7c3aed,stroke:#6d28d9,color:#fff
    style P fill:#ec4899,stroke:#db2777,color:#fff
```

## Data Flow
```mermaid
sequenceDiagram
    participant User
    participant API
    participant SpoonOS
    participant Agents
    participant Neo
    
    User->>API: Request volatility
    API->>SpoonOS: Orchestrate workflow
    
    SpoonOS->>Agents: Task 1: Fetch prices
    Agents-->>SpoonOS: Price data
    
    SpoonOS->>Agents: Task 2: Calculate vol
    Agents-->>SpoonOS: 7 estimators
    
    SpoonOS->>Agents: Task 3: GARCH forecast
    Agents-->>SpoonOS: Prediction
    
    SpoonOS->>Agents: Task 4: Publish
    Agents->>Neo: Update contract
    Neo-->>Agents: Transaction hash
    
    Agents-->>API: Complete result
    API-->>User: Volatility data
```

## Component Details

### SpoonOS Agents

| Agent | Responsibility | Dependencies | Output |
|-------|----------------|--------------|--------|
| Market Data Collector | Fetch OHLCV from DEXs | None | Price feeds |
| Volatility Calculator | Compute 7 estimators | Market Data | RV estimates |
| Implied Vol Engine | Build vol surface | Market Data | IV surface |
| GARCH Forecaster | Time series prediction | Volatility Calc | Forecast |
| Arbitrage Detector | Find IV-RV spread | Vol Calc plus IV | Signals |
| Neo Publisher | Write to blockchain | All agents | Tx hash |

### Performance Optimizations
```mermaid
graph LR
    A[Python API] -->|Hot Path| B[C++ Engine]
    B -->|100x faster| C[Black-Scholes]
    
    A -->|GARCH| D[OCaml Engine]
    D -->|Type Safety| E[Volatility Models]
    
    A -->|ML| F[TensorFlow]
    F -->|GPU Accel| G[LSTM/XGBoost]
    
    style B fill:#ef4444,stroke:#dc2626,color:#fff
    style D fill:#f59e0b,stroke:#d97706,color:#fff
    style F fill:#10b981,stroke:#059669,color:#fff
```
