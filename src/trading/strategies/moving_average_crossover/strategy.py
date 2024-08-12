from ..strategy_base import BaseStrategy
from typing import Dict, Any
import numpy as np


class MovingAverageCrossover(BaseStrategy):
    '''
    The Moving Average Crossover strategy is a popular technical analysis technique used in trading. This implementation, encapsulated in the `MovingAverageCrossover` class, generates buy and sell signals based on the crossover of short-term and long-term moving averages.
    '''

    def initialize(self, parameters: Dict[str, Any]):
        self.short_window = parameters.get('short_window', 10)
        self.long_window = parameters.get('long_window', 30)
        self.data = []

    def on_market_data(self, data: Dict[str, Any]):
        self.data.append(data['close'])
        if len(self.data) > self.long_window:
            self.data.pop(0)

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
