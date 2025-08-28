import requests
import geopandas as gpd
from shapely.geometry import shape
import pandas as pd
import matplotlib.pyplot as plt
from enum import Enum

def create_map_unit(state:str, mtype:str) -> None:
    "This script creates an instance of the MapUnit class corresponding to <state> and <map_type>."

    if mtype == 'proposed':
        map_name = 'proposed'
        map_path = '../data/orange_3/UT-C21Dist-O3.geojson'
        score_path = 'https://redistricting-report-card.s3.amazonaws.com/UT/congressional/2020-census/results/plan-scores/UT-C21Dist-O3.json'
    
    elif mtype == 'enacted':
        map_name = 'enacted'
        map_path='../data/enacted/UT-Utah-congressional-DRA.geojson',
        score_path='https://redistricting-report-card.s3.amazonaws.com/UT/congressional/2020-census/results/plan-report-cards/UT-Utah-congressional-DRA-report-card.json'

    obj = MapUnit(state = state,
                  mtype=mtype,
                  map_name = map_name,
                  map_path = map_path,
                  score_path = score_path)
    return obj
    
class MapUnit:
    """This is the general class to hold data about each type of congressional district map (enacted and different draft versions).
    To create an instance, pass:
    - name ('enacted','draft orange' ...),
    - path to locally downloaded district polygons
    - path to json of scores (from Princteon Gerrymander project)
    """
    _VALID_STATES = ["Utah", "utah","UT"]
    _VALID_TYPES = ['Enacted','enacted','Proposed','proposed']
    def __init__(self, 
                 state: str,
                 mtype:str,
                 map_name:str, 
                 map_path:str,
                 score_path:str):
        
        if state not in self._VALID_STATES:
            raise NotImplementedError(f"{state} not implemented. Must be one of {','.join(self._VALID_STATES)}")
        if mtype not in self._VALID_TYPES:
            raise NotImplementedError(f"{mtype} not implemented. Must be one of {','.join(self._VALID_TYPES)}")
        self.state = state
        self.map_type = mtype
        self.map_name = map_name
        self.map_path = map_path
        self.score_path = score_path
        self._map = None
        self._score_df = None
        self._final_score = None

    @property
    def districts_map(self):
        if self._map is None:
            self._map = self.create_districts_map()
        return self._map
    
    def create_districts_map(self):
        print('here')
        map_gdf = gpd.read_file(self.map_path)
        return map_gdf
    
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
        if self.map_type == 'enacted':
        #if 'finalReportCardGrade' in score_df.columns:
            final_score = score_df.loc['finalReportCardGrade']['report_card']
        else:
            raise NotImplementedError('Scores only available for enacted maps.')
        return final_score