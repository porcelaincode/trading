# Moving Average Crossover Strategy Documentation

## Overview

The Moving Average Crossover strategy is a popular technical analysis technique used in trading. This implementation, encapsulated in the `MovingAverageCrossover` class, generates buy and sell signals based on the crossover of short-term and long-term moving averages.

## Class Definition

```python
class MovingAverageCrossover(BaseStrategy):
    # ... methods ...
```

The `MovingAverageCrossover` class inherits from a `BaseStrategy` class, suggesting it's part of a larger trading strategy framework.

## Key Methods

### 1. initialize

```python
def initialize(self, parameters: Dict[str, Any]):
    self.short_window = parameters.get('short_window', 10)
    self.long_window = parameters.get('long_window', 30)
    self.data = []
```

This method initializes the strategy with user-defined parameters:

- `short_window`: The period for the short-term moving average (default: 10)
- `long_window`: The period for the long-term moving average (default: 30)
- `data`: An empty list to store closing prices

### 2. on_market_data

```python
def on_market_data(self, data: Dict[str, Any]):
    self.data.append(data['close'])
    if len(self.data) > self.long_window:
        self.data.pop(0)
```

This method is called when new market data is received:

- Appends the closing price to the `data` list
- Maintains the list size equal to `long_window` by removing the oldest data point if necessary

### 3. generate_signal

```python
def generate_signal(self) -> Dict[str, Any]:
    if len(self.data) < self.long_window:
        return {'action': 'WAIT'}
    short_ma = np.mean(self.data[-self.short_window:])
    long_ma = np.mean(self.data[-self.long_window:])
    if short_ma > long_ma:
        return {'action': 'BUY'}
    elif short_ma < long_ma:
        return {'action': 'SELL'}
    else:
        return {'action': 'HOLD'}
```

This method generates trading signals based on the moving average crossover:

- Calculates short-term and long-term moving averages
- Returns 'BUY' when short-term MA crosses above long-term MA
- Returns 'SELL' when short-term MA crosses below long-term MA
- Returns 'HOLD' when there's no crossover
- Returns 'WAIT' if there's insufficient data

## Strategy Logic

1. The strategy waits until it has collected enough data points (equal to `long_window`).
2. It calculates two moving averages:
   - Short-term MA: average of the last `short_window` closing prices
   - Long-term MA: average of the last `long_window` closing prices
3. It generates signals based on the relative positions of these moving averages:
   - BUY: Short-term MA above Long-term MA
   - SELL: Short-term MA below Long-term MA
   - HOLD: Short-term MA equal to Long-term MA

## Usage

To use the Moving Average Crossover Strategy:

1. Initialize the strategy with desired parameters:

```python
strategy = MovingAverageCrossover()
strategy.initialize({
    'short_window': 10,
    'long_window': 30
})
```

2. Feed market data to the strategy:

```python
strategy.on_market_data({'close': 100.0})  # Repeat for each new data point
```

3. Generate trading signals:

```python
signal = strategy.generate_signal()
```

4. Interpret the returned signal:
   - 'BUY': Open a long position or close a short position
   - 'SELL': Open a short position or close a long position
   - 'HOLD': No action required
   - 'WAIT': Insufficient data to generate a signal

## Notes

- The strategy uses NumPy for calculating moving averages.
- It assumes a constant stream of closing price data.
- The effectiveness of the strategy can vary depending on the chosen window sizes and market conditions.

## Limitations and Considerations

- The strategy does not implement position sizing or risk management.
- It does not account for transaction costs or slippage.
- The simple moving average is equally weighted, which may not be ideal for all market conditions.
- The strategy may generate frequent signals in choppy markets, potentially leading to overtrading.
