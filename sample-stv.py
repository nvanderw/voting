import random
from proportional import stv
from util import shuffled
from misc.players import all_players

# Example election: voters are purely partisan and vote for their party's candidates in random order
if __name__ == "__main__":
    parties = {}
    num_approx_candidates = 100

    for player in all_players:
        if random.random() > num_approx_candidates / len(all_players):
            continue
        if player.team not in parties:
            parties[player.team] = [player.name]
        else:
            parties[player.team].append(player.name)

    ballots = []
    party_sizes = {}
    for party in parties:
        party_sizes[party] = random.randrange(100, 5000)
        for voter in range(party_sizes[party]):
            ballots.append([f"({party}) {c}" for c in shuffled(parties[party])])

    print(f"Voters in each party: {party_sizes}")
    print(f"Resulting seats: {stv(5, ballots)}")
