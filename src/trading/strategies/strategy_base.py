from abc import ABC, abstractmethod
from typing import Dict, Any

from moving_average_crossover import MovingAverageCrossover


class BaseStrategy(ABC):
    @abstractmethod
    def initialize(self, parameters: Dict[str, Any]):
        """Initialize the strategy with given parameters."""
        pass

    @abstractmethod
    def on_market_data(self, data: Dict[str, Any]):
        """Process incoming market data."""
        pass

    @abstractmethod
    def generate_signal(self) -> Dict[str, Any]:
        """Generate trading signal based on processed data."""
        pass
