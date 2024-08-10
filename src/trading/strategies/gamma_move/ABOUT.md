# Gamma Catcher Strategy Documentation

## Overview

The Gamma Catcher Strategy is an options trading strategy that aims to capitalize on high gamma opportunities while managing vega exposure. This strategy is implemented in the `GammaCatcherStrategy` class, which inherits from a base strategy class.

## Key Components

### 1. OptionData

A dataclass that represents the essential data for an option:

```python
@dataclass
class OptionData:
    symbol: str
    strike: float
    expiry: float  # Time to expiry in days
    option_type: str  # 'call' or 'put'
    underlying_price: float
    option_price: float
    implied_volatility: float
```

### 2. GammaCatcherStrategy

The main class that implements the strategy:

```python
class GammaCatcherStrategy(BaseStrategy):
    def __init__(self, risk_free_rate: float, gamma_threshold: float,
                 vega_threshold: float, lot_size: int):
        # ... initialization ...
```

## Key Methods

### 1. calculate_option_greeks

Calculates the Greeks (delta, gamma, vega, theta) for a given option using the Black-Scholes model.

### 2. analyze_options

Analyzes a list of options by calculating their Greeks and gamma-to-vega ratios.

### 3. generate_signal

Generates trading signals based on the analyzed options and predefined thresholds.

### 4. update_positions

Updates the strategy's positions based on the generated signals.

### 5. run

The main method that executes the strategy for a given list of options.

## Strategy Logic

1. **Entry Criteria:**

   - Gamma > gamma_threshold
   - |Vega| < vega_threshold
   - Gamma-to-Vega ratio > 1

2. **Exit Criteria:**

   - Gamma < gamma_threshold / 2
   - |Vega| > vega_threshold \* 2

3. **Position Sizing:**
   - Uses a predefined lot_size for each trade

## Usage

To use the Gamma Catcher Strategy:

1. Initialize the strategy with desired parameters:

```python
strategy = GammaCatcherStrategy(
    risk_free_rate=0.02,
    gamma_threshold=0.1,
    vega_threshold=0.05,
    lot_size=100
)
```

2. Prepare a list of OptionData objects with current market data.

3. Run the strategy:

```python
signal = strategy.run(options_data)
```

4. Interpret the returned signal:
   - 'BUY': Open a new position
   - 'SELL': Close an existing position
   - 'HOLD': No action required

## Notes

- The strategy uses the Black-Scholes model for options pricing and Greeks calculation.
- It's important to carefully choose the gamma_threshold and vega_threshold based on market conditions and risk tolerance.
- The strategy assumes a constant risk-free rate and uses a 365-day year for time-to-expiry calculations.

## Limitations and Considerations

- The strategy does not account for transaction costs or slippage.
- It does not implement any portfolio-wide risk management techniques.
- The effectiveness of the strategy may vary depending on market conditions and the accuracy of implied volatility estimates.
