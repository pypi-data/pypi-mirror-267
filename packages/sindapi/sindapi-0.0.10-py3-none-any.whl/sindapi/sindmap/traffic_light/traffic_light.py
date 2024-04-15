
from enum import Enum, unique
from dataclasses import dataclass
from typing import Dict, List, Optional

from ..stretch.stretch import Stretch
from ..intersection.intersection import Intersection



@unique
class SignalType(int, Enum):
    """All traffic lights are assigned one of the signal type labels."""

    RED: int = 0
    YELLOW: int = 3
    GREEN: int = 1
    UNKNOWN: int = 2    # it is stupid to assign 3-YELLOW 2-UNKNOWN, but it is the way they defined in SinD rawdata
                        # by the way, there is no definition of UNKNOWN type in SinD, only 0,1,3

    @classmethod
    def from_int(cls, number: int) -> 'SignalType':
        """Converts a number to SignalType."""
        for signal_type in cls:
            if signal_type.value == number:
                return signal_type
        raise ValueError(f"No SignalType found for number {number}")


@dataclass
class LightState:
    """Bundles all state information associated with an object at a fixed point in time.

    Attributes:
        timestep: Time step corresponding to this object state [0, num_scenario_timesteps).
        signal_type: SignalType of the light
        remaining_seconds: Number of seconds remaining
    """

    timestep: int
    signal_type: SignalType
    remaining_seconds: int



@dataclass
class TrafficLight:
    id: int
    controlled_stretches: List[int]
    controlled_intersections: List[int]
    light_states: List[LightState]

