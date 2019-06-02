import sys
sys.path.append("../")
import shading_preamble
from typing import Dict


"""other constants"""
constants: Dict = {
    "FLOOR_HEIGHT": 2.8,
    "WINDOW_HEIGHT": 1.5,
    "WINDOW_EDGT_HEIGHT": 1
}

"""path constants"""
paths: Dict = {
    "WEATHER_FILE": "./WeatherData/CHN_Chongqing.Chongqing.Shapingba.575160_CSWD.epw",
    "IDF_FILE": "../shading_model2.idf",
    "OUTPUT_PATH": "temp/",
}


p = shading_preamble.ShadingPreamble(constants, paths)
p(2, 2, 2, 0.15, 0.15, 0.15, 0.15, 233, 10, 2.3, 2)
