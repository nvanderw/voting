import csv
import itertools
import sys
import os
import os.path
import random
from dataclasses import dataclass
from io import TextIOWrapper
from typing import List, Optional


@dataclass
class Player:
    position: str
    extra_pos: Optional[str]
    team: str
    name: str


def _parse_mcmxciv_fighting_baseball_snes_japan_full_rosters_csv_file(mcmxciv_fighting_baseball_snes_japan_full_rosters_csv_reader: TextIOWrapper) -> List[Player]:
    header = next(mcmxciv_fighting_baseball_snes_japan_full_rosters_csv_reader)
    teams = header[1:]
    players = []
    for row in mcmxciv_fighting_baseball_snes_japan_full_rosters_csv_reader:
        position = row[0]
        for team, name in zip(teams, row[1:]):
            name_components = name.split()
            if len(name_components) > 2:
                extra_pos = name_components[0]
                name = ' '.join(name_components[1:])
            else:
                extra_pos = None

            player = Player(position, extra_pos, team, name)
            players.append(player)

    return players


def _get_players():
    with open(os.path.join(os.path.dirname(sys.modules[__name__].__file__), '1994 Fighting Baseball (SNES) Japan Full Rosters - Rosters.csv')) as mcmxciv_fighting_baseball_snes_japan_full_rosters_csv_file:
        mcmxciv_fighting_baseball_snes_japan_full_rosters_csv_reader = csv.reader(
            mcmxciv_fighting_baseball_snes_japan_full_rosters_csv_file)
        return _parse_mcmxciv_fighting_baseball_snes_japan_full_rosters_csv_file(mcmxciv_fighting_baseball_snes_japan_full_rosters_csv_reader)


all_players = _get_players()
all_first_names = set(player.name.split()[0] for player in all_players)
all_last_names = set(player.name.split()[1] for player in all_players)

# generates a sequence of 204,910 mashup names


def get_random_baseball_names():
    def shuffled(seq):
        lst = [*seq]
        random.shuffle(lst)
        return lst

    return (f"{first_name} {last_name}" for first_name, last_name in shuffled(itertools.product(all_first_names, all_last_names)))
