# <Copyright 2022, Argo AI, LLC. Released under the MIT license.>

"""Constants used throughout the AV2 motion forecasting API."""

from typing import Final

SIND_SCENARIO_OBS_TIMESTEPS: Final[int] = 10
SIND_SCENARIO_PRED_TIMESTEPS: Final[int] = 10
SIND_SCENARIO_TOTAL_TIMESTEPS: Final[int] = SIND_SCENARIO_OBS_TIMESTEPS + SIND_SCENARIO_PRED_TIMESTEPS
SIND_SCENARIO_GENERATION_STEP: Final[int] = 3

SIND_SCENARIO_RECORD_STEP_HZ: Final[float] = 29.97
SIND_SCENARIO_TRACK_STEP_HZ: Final[int] = 10
SIND_SCENARIO_TRAFFICLIGHT_STEP_HZ: Final[int] = 30
