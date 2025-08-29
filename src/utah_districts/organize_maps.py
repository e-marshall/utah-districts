import pandas as pd
from dataclasses import dataclass
from typing import Type

### ----- Data layer ----- ###
#--------- These communicate to the 'database' ---------#
# Will hold readers/paths? 
# Will also hold df so that only the data needed in the domain model is there? 
class EnactedMapReader:
    """This class would be in the 'database layer'? or interface?
    It knows the path that points to the enacted map json and reads it into memory
    """
    def __init__(self, path:str):
        self.path = path
        self.read_df()

    def read_df(self):

        self.df = pd.read_json(self.path)

class ProposedMapReader:
    """This class would be in the 'database layer'? or interface?
    It knows the path that points to the enacted map json and reads it into memory
    """
    def __init__(self, path):
        self.path = path
        self.read_df()

    def read_df(self):

        self.df = pd.read_json(self.path)

def make_both_readers(enacted_reader = EnactedMapReader,
                      proposed_reader = ProposedMapReader):
    """This function reads the paths to 2 json files and returns two Reader objs"""

    enacted_df_path = "https://redistricting-report-card.s3.amazonaws.com/UT/congressional/2020-census/results/plan-report-cards/UT-Utah-congressional-DRA-report-card.json"
    proposed_df_path ="https://redistricting-report-card.s3.amazonaws.com/UT/congressional/2020-census/results/plan-scores/UT-C21Dist-O3.json"

    enacted = enacted_reader(path = enacted_df_path)
    assert isinstance(enacted, EnactedMapReader), 'enacted_reader not an EnactedReader'
    proposed = proposed_reader(path = proposed_df_path)

    return (enacted, proposed)

#--------- These are the components of the data model ---------#    
class EnactedMapRepository:
    """This class holds the data about the enacted map that is relevant to the domain.
    It communicates with the reader, which holds the full df"""
    def __init__(self, reader: EnactedMapReader):
        assert isinstance(reader, EnactedMapReader), f'reader obj, expected: EnactedMapReader, received: {type(reader)}.'
        assert isinstance(reader.df, pd.DataFrame), f'Expected: EnactedMapReader, received: {type(reader)}'
        self.df = reader.df
        self.calc_score()
        self.calc_compactness()

    def calc_score(self):
        """graded score for the enacted map"""

        expected_col = "finalReportCardGrade"
        assert expected_col in self.df.columns, f'{expected_col} not in df.columns'

        final_score = self.df.loc[expected_col]["report_card"]

        self.score =  final_score
    
    def calc_compactness(self):
        """Compactness score for either map (should maybe structure these classes differently)"""

        expected_col = "plan"
        expected_idx = "avgReock"

        assert expected_col in self.df, f'{expected_col} not in df.columns'

        avg_reock = self.df.loc[expected_idx][expected_idx]
        self.compactness = avg_reock
        
class ProposedMapRepository:
    """This class holds the data about the enacted map that is relevant to the domain.
    It communicates with the reader, which holds the full df"""
    def __init__(self, reader: ProposedMapReader):

        self.df = reader.df
        self._score = None
        self._compactness = None

        @property
        def score(self):
            """graded score for the enacted map"""
            if self._score is None:
                self._score = self.get_score()
            return self._score
        
        def get_score(self):
            """Get the graded score for the enacted map"""
            expected_col = "finalReportCardGrade"
            assert expected_col in self.df.columns, f'{expected_col} not in df.columns'

            final_score = self.df.loc[expected_col]["report_card"]

            return final_score
        
        @property
        def compactness(self):
            """Compactness score for either map (should maybe structure these classes differently)"""
            if self._compactness is None:
                self._compactness = self.get_copmactness()
            return self._compactness
        
        def get_compactness(self):
            """Get the compactness score for the map"""
            expected_col = "plan"
            expected_idx = "avgReock"

            assert expected_col in self.df, f'{expected_col} not in df.columns'

            avg_reock = self.df.loc[expected_idx][expected_idx]
            return avg_reock
        
### ----- Domain layer ----- ###
@dataclass
class StateData:
    name: str
    enacted_map: EnactedMapRepository  
    proposed_map: ProposedMapRepository
    #score = EnactedMapRepository.score

    def get_enacted_compactness(self):
        print('enacted map compactness: ', self.enacted_map.compactness)
    def compare_compactness(self): 
        self.compactness_diff = self.proposed_map.compactness - self.enacted_map.compactness


def make_both_repos():
    """This method """

    enacted_reader, proposed_reader = make_both_readers()
    assert isinstance(enacted_reader, EnactedMapReader), 'Problem'
    enacted_repo = EnactedMapRepository(enacted_reader)
    proposed_repo = ProposedMapRepository(proposed_reader)

    return (enacted_repo, proposed_repo)

def make_state_data_obj(name:str = "Utah"):

    #make repos
    enacted_repo, proposed_repo = make_both_repos()

    #then, make state data
    state_data = StateData(name,enacted_repo, proposed_repo)

    return state_data

def test_compare_compactness_returns_correct_diff():

    state_data = make_state_data_obj() 
    return state_data

