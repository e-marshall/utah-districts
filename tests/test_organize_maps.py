from utah_districts.organize_maps import create_map_unit


def test_create_map():
    for mtype in ["enacted", "proposed"]:
        obj = create_map_unit(state="Utah", mtype=mtype)
        assert obj.map_type == mtype
        assert obj.map_name == mtype
