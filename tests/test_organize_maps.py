from utah_districts import organize_maps
import pytest
import pandas as pd

def test_compare_compactness_returns_correct_diff():

    state_data = organize_maps.make_state_data_obj() 

    state_data.enacted_map.compactness = 0.25
    state_data.proposed_map.compactness = 0.6

    expected_diff = 0.6 - 0.25

    actual_diff = state_data.compare_compactness()

    assert expected_diff == actual_diff, f'{expected_diff} != {actual_diff}'

class MockReader:
    def __init__(self, path:str = 'mock/file.json'):
        self.path = path
        self.df = pd.DataFrame({'Index':'avgReock',
                                'plan': 0.5}, index=[0])

def test_make_both_readers():

    enacted, proposed = organize_maps.make_both_readers(MockReader,
                                          MockReader)
    #TODO MockReader needs to type math EnactedMapReader? how? may make both subclasses of an abc?
    assert isinstance(enacted, MockReader)
    assert isinstance(proposed, MockReader)

    assert enacted.path.endswith('.json')
    assert proposed.path.endswith('.json')

    assert isinstance(enacted.df, pd.DataFrame)
    assert isinstance(proposed.df, pd.DataFrame)

class MockRepo:
    def __init__(self, MockReader):
        self.df = MockReader.df
        self.score = 'B'
        self.compactness = self.df.iloc[0]['plan']


