from abc import ABC, abstractmethod
from swarmauri.standard.metrics.base.CalculateMetricBase import CalculateMetricBase
from swarmauri.core.metrics.IAggMeasurements import IAggMeasurements

class AggregateMetricBase(CalculateMetricBase, IAggMeasurements, ABC):
    """
    An abstract base class that implements the IMetric interface, providing common 
    functionalities and properties for metrics within SwarmAURI.
    """
    def __init__(self, name: str, *args, **kwargs):
        CalculateMetricBase.__init__(name)
        self._dataset = []

    @abstractmethod
    def add_measurement(self, *args, **kwargs) -> None:
        raise NotImplementedError('Measurement not implemented')

    def reset(self) -> None:
        """
        Resets the metric's state/value, allowing for fresh calculations.
        """
        self._value = None

