from .strategy_base import BaseStrategy
from typing import Dict, List, Any
from dataclasses import dataclass
import numpy as np
from scipy.stats import norm


@dataclass
class OptionData:
    symbol: str
    strike: float
    expiry: float  # Time to expiry in days
    option_type: str  # 'call' or 'put'
    underlying_price: float
    option_price: float
    implied_volatility: float


def days_to_years(days: int) -> float:
    return days / 365.0


class GammaCatcherStrategy(BaseStrategy):
    def __init__(self, risk_free_rate: float, gamma_threshold: float,
                 vega_threshold: float, lot_size: int):
        self.risk_free_rate = risk_free_rate
        self.gamma_threshold = gamma_threshold
        self.vega_threshold = vega_threshold
        self.lot_size = lot_size
        self.positions: Dict[str, int] = {}

    def calculate_option_greeks(self, option: OptionData) -> Dict[str, float]:
        S = option.underlying_price
        K = option.strike
        T = days_to_years(option.expiry)
        r = self.risk_free_rate
        sigma = option.implied_volatility

        d1 = (np.log(S/K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        if option.option_type == 'call':
            delta = norm.cdf(d1)
            gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
            vega = S * norm.pdf(d1) * np.sqrt(T)
            theta = -S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - \
                r * K * np.exp(-r * T) * norm.cdf(d2)
        else:  # put
            delta = -norm.cdf(-d1)
            gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
            vega = S * norm.pdf(d1) * np.sqrt(T)
            theta = -S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) + \
                r * K * np.exp(-r * T) * norm.cdf(-d2)

        return {
            'delta': delta,
            'gamma': gamma,
            'vega': vega,
            'theta': theta
        }

    def analyze_options(self, options: List[OptionData]) -> List[Dict[str, Any]]:
        analyzed_options = []
        for option in options:
            greeks = self.calculate_option_greeks(option)
            analyzed_options.append({
                'option': option,
                'greeks': greeks,
                'gamma_to_vega_ratio': greeks['gamma'] / greeks['vega'] if greeks['vega'] != 0 else float('inf')
            })
        return analyzed_options

    def generate_signal(self, analyzed_options: List[Dict[str, Any]]) -> Dict[str, Any]:
        for analyzed_option in analyzed_options:
            option = analyzed_option['option']
            greeks = analyzed_option['greeks']
            gamma_to_vega_ratio = analyzed_option['gamma_to_vega_ratio']

            if (greeks['gamma'] > self.gamma_threshold and
                abs(greeks['vega']) < self.vega_threshold and
                    gamma_to_vega_ratio > 1):

                # Check if we already have a position
                current_position = self.positions.get(option.symbol, 0)

                if current_position == 0:
                    return {
                        'action': 'BUY',
                        'option': option,
                        'quantity': self.lot_size,
                        'reason': 'High gamma, low vega, favorable gamma-to-vega ratio'
                    }

            elif option.symbol in self.positions:
                # Check for exit conditions
                if (greeks['gamma'] < self.gamma_threshold / 2 or
                        abs(greeks['vega']) > self.vega_threshold * 2):
                    return {
                        'action': 'SELL',
                        'option': option,
                        'quantity': self.positions[option.symbol],
                        'reason': 'Exit conditions met'
                    }

        return {'action': 'HOLD'}

    def update_positions(self, signal: Dict[str, Any]):
        if signal['action'] in ['BUY', 'SELL']:
            option = signal['option']
            quantity = signal['quantity']
            if signal['action'] == 'BUY':
                self.positions[option.symbol] = self.positions.get(
                    option.symbol, 0) + quantity
            else:  # SELL
                self.positions[option.symbol] = max(
                    0, self.positions.get(option.symbol, 0) - quantity)
                if self.positions[option.symbol] == 0:
                    del self.positions[option.symbol]

    def run(self, options_data: List[OptionData]) -> Dict[str, Any]:
        analyzed_options = self.analyze_options(options_data)
        signal = self.generate_signal(analyzed_options)
        self.update_positions(signal)
        return signal
