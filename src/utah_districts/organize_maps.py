import geopandas as gpd

# from shapely.geometry import shape
import pandas as pd

# import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Literal
from enum import Enum


def create_score_obj(state: str, mtype: str) -> None:
    maptype = MapType


def create_map_unit(state: str, mtype: str) -> None:
    "This script creates an instance of the MapUnit class corresponding to <state> and <map_type>."

    if mtype == "proposed":
        map_name = "proposed"
        map_path = "../data/orange_3/UT-C21Dist-O3.geojson"
        score_path = "https://redistricting-report-card.s3.amazonaws.com/UT/congressional/2020-census/results/plan-scores/UT-C21Dist-O3.json"

    elif mtype == "enacted":
        map_name = "enacted"
        map_path = ("../data/enacted/UT-Utah-congressional-DRA.geojson",)
        score_path = "https://redistricting-report-card.s3.amazonaws.com/UT/congressional/2020-census/results/plan-report-cards/UT-Utah-congressional-DRA-report-card.json"

    obj = MapUnit(
        state=state,
        mtype=mtype,
        map_name=map_name,
        map_path=map_path,
        score_path=score_path,
    )
    return obj


class MapType(str, Enum):
    """Class to hold attr of whether a map unit obj is enacted or proposed"""

    ENACTED = "enacted"
    PROPOSED = "proposed"


class DataType(str, Enum):
    """Class to hold attr of whether a data component is map or score"""

    MAP = "map"
    SCORE = "score"


@dataclass
class UnitParams:
    """Class to hold input params used to define a Map and Score objs."""

    state: str
    map_type: MapType
    data_path: str
    data_type: DataType


class Map:
    def __init__(self, unit_params: UnitParams):
        self.state = unit_params.state
        self.map_type = unit_params.map_type
        self.map_path = unit_params.data_path
        self._map_gdf = None

    @property
    def map_gdf(self):
        if self._map_gdf is None:
            self._map_gdf = self.create_map()
        return self._map_gdf

    def create_map(self):
        print("here")
        map_gdf = gpd.read_file(self.map_path)
        return map_gdf


class Score:
    def __init__(self, unit_params: UnitParams):
        self.state = unit_params.state
        self.map_type = unit_params.map_type
        self.score_path = unit_params.data_path
        self._score_df = None
        self._final_score = None

    @property
    def score_df(self):
        if self._score_df is None:
            self._score_df = self.read_score_df()
        return self._score_df

    def read_score_df(self):
        score_df = pd.read_json(self.score_path)
        return score_df

    @property
    def final_score(self):
        if self._final_score is None:
            self._final_score = self.get_final_score()
        return self._final_score

    def get_final_score(self):
        score_df = self.score_df
        if self.map_type == "enacted":
            # if 'finalReportCardGrade' in score_df.columns:
            final_score = score_df.loc["finalReportCardGrade"]["report_card"]
        else:
            raise NotImplementedError("Scores only available for enacted maps.")
        return final_score


class DistrictMapUnit:
    def __init__(self, map_obj, score_obj):
        self.state = map_obj.state
        self.map_type = map_obj.map_type
        self.map_gdf = map_obj.map_gdf
        self.score_df = score_obj.score_df