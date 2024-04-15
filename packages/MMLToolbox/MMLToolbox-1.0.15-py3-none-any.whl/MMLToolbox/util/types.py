from typing import Type, Union, Dict, Any, List, Tuple, Callable
from numpy import ndarray


# Device Types
EPSTEIN = "epstein"
BHC = "bhc"
PBHC = "pbhc"
DEFAULT = ""

# Device Parameter
EPSTEIN_PARAM = {"B_turns": (700, "-"),
                 "H_turns": (700, "-"),
                 "l_eff": (0.94, "m"),
                 "Rohrer_voltage_factor": (100, "V/V"),
                 "Rohrer_current_factor": (10, "A/V")}

BHC_PARAM = {"B_turns": (3, "-"),
             "B_amp": (1, "-"),
             "H_turns": (170, "-"),
             "H_area": (19.385e-6, "m^2"),
             "H_amp": (1, "-"),
             "Hx_factor": (1.39, "-"),
             "Hy_factor": (1.34, "-"),
             "Hall_factor": (1/50, "-"),
             "Rohrer_voltage_factor": (100, "V/V"),
             "Rohrer_current_factor": (10, "A/V")}

PBHC_PARAM = {"B_turns": (1, "-"),
              "B_amp": (200, "-"),
              "Bx_factor": (1, "-"),
              "By_factor": (1, "-"),

              "Hx_upper_turns": (51, "-"),
              "Hx_upper_area": (0.022*0.0003, "m^2"),
              "Hx_upper_amp": (500, "-"),
              "Hx_upper_factor": (1, "-"),

              "Hy_upper_turns": (52, "-"),
              "Hy_upper_area": (0.023*0.0003, "m^2"),
              "Hy_upper_amp": (500, "-"),
              "Hy_upper_factor": (1, "-"),

              "Hx_bottom_turns": (51, "-"),
              "Hx_bottom_area": (0.022*0.0003, "m^2"),
              "Hx_bottom_amp": (500, "-"),
              "Hx_bottom_factor": (1, "-"),

              "Hy_bottom_turns": (52, "-"),
              "Hy_bottom_area": (0.023*0.0003, "m^2"),
              "Hy_bottom_amp": (500, "-"),
              "Hy_bottom_factor": (1, "-"),

              "Hall_factor": (1/50, "-"),

              "Rohrer_voltage_factor": (100, "V/V"),
              "Rohrer_current_factor": (10, "A/V")}