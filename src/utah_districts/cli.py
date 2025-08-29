import click
import numpy as np

from utah_districts.organize_maps import make_state_data_obj


@click.group()
def main():
    pass


@main.command("see-score")
@click.option(
    "--state",
    # prompt = 'Enter a state',
    default="Utah",
    help="Choose one of the U.S. states to see its gerrymander score",
)
def see_score(state: str):
    map_obj = make_state_data_obj(state)
    score = map_obj.enacted_map.score
    text = click.wrap_text(f"{state}'s gerrymandering score is: {score}")
    click.echo(text)
    return map_obj.final_score


@main.command("see-compactness")
@click.option(
    "--state",
    # prompt = 'Enter a state',
    default="Utah",
    help="Choose one of the U.S. states to see its gerrymander score",
)
@click.option(
    "--mtype",
    default="enacted",
    type=click.Choice(["enacted", "proposed"], case_sensitive=False),
    help="Type of congressional map you'd like to see (enacted or proposed)",
)
def see_compactness(state: str, mtype: str):
    map_obj = make_state_data_obj(state)
    if mtype == 'enacted':
        compactness = map_obj.enacted_map.compactness
    elif mtype == 'proposed':
        compactness = map_obj.proposed_map.compactness 
    text = click.wrap_text(
        f"{state}'s {mtype} map had an avg. reock (compactness score) of {compactness}. 0 is not compact; 1 is optimally compact."
    )
    click.echo(text)


#@main.command("compare-compactness")
#@click.option(
#    "--state",
#    # prompt = 'Enter a state',
#    default="Utah",
#    help="Choose one of the U.S. states to see its gerrymander score",
#)

#def compare_proposed_enacted(state: str):
#    enacted_map = create_map_unit(state, "enacted")
#    enacted_df = enacted_map.score_df
#    enacted_reock = np.round(enacted_df.loc["avgReock"]["plan"], 4)

#    proposed_map = create_map_unit(state, "proposed")
#    proposed_df = proposed_map.score_df
#    proposed_reock = np.round(proposed_df.loc["avgReock"]["plan"], 4)

#    text = click.wrap_text(
#        f"Compactness of proposed map: {proposed_reock} v. compactness of enacted map: {enacted_reock} (Remember 1 = optimally compact)."
#    )
#    click.echo(text)