import pytest
from utah_districts.organize_maps import create_map_unit, MapUnit

def test_create_map():

    for mtype in ['enacted','proposed']:
        obj = create_map_unit(state='Utah',
                              mtype=mtype)
        assert obj.map_type == mtype
        assert obj.map_name == mtype

def test_maps():

    map_unit = MapUnit(
        state="Utah",
        mtype="enacted",
        map_name = "enacted",
        map_p
    )