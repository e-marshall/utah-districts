import click
import numpy as np

from utah_districts.organize_maps import create_map_unit


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
@click.option(
    "--mtype",
    default="enacted",
    type=click.Choice(["enacted", "proposed"], case_sensitive=False),
    help="Type of congressional map you'd like to see (enacted or proposed)",
)
def see_score(state: str, mtype: str):
    map_obj = create_map_unit(state, mtype)
    score = map_obj.final_score
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
    map_obj = create_map_unit(state, mtype)
    score_df = map_obj.score_df
    avg_reock = score_df.loc["avgReock"]["plan"]
    text = click.wrap_text(
        f"{state}'s {mtype} map had an avg. reock (compactness score) of {avg_reock}. 0 is not compact; 1 is optimally compact."
    )
    click.echo(text)


@main.command("compare-compactness")
@click.option(
    "--state",
    # prompt = 'Enter a state',
    default="Utah",
    help="Choose one of the U.S. states to see its gerrymander score",
)
def compare_proposed_enacted(state: str):
    enacted_map = create_map_unit(state, "enacted")
    enacted_df = enacted_map.score_df
    enacted_reock = np.round(enacted_df.loc["avgReock"]["plan"], 4)

    proposed_map = create_map_unit(state, "proposed")
    proposed_df = proposed_map.score_df
    proposed_reock = np.round(proposed_df.loc["avgReock"]["plan"], 4)

    text = click.wrap_text(
        f"Compactness of proposed map: {proposed_reock} v. compactness of enacted map: {enacted_reock} (Remember 1 = optimally compact)."
    )
    click.echo(text)
