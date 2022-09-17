import random
from proportional import stv

# Example election: voters are purely partisan and vote for their party's candidates in random order
if __name__ == '__main__':
    def shuffled(seq):
        l = list(seq)
        random.shuffle(l)
        return l

    parties = {
        "Red": [
            "Sleve McDichael",
            "Onson Sweemey",
            "Darryl Archideld",
            "Anatoli Smorin",
            "Rey McSriff",
            "Glenallen Mixon",
            "Mario McRlwain",
        ],
        "Green": [
            "Raul Chamgerlain",
            "Kevin Nogilny",
            "Tony Smehrik",
            "Bobson Dugnutt",
            "Willie Dustice",
            "Jeromy Gride",
            "Scott Dourque",
        ],
        "Blue": [
            "Shown Furcotte",
            "Dean Wesrey",
            "Mike Truk",
            "Dwigt Rortugal",
            "Tim Sandaele",
            "Karl Dandleton",
            "Mike Sernandez",
            "Todd Bonzalez"
        ]
    }

    ballots = []
    party_sizes = {}
    for party in parties:
        party_sizes[party] = random.randrange(5000, 15001)
        for voter in range(party_sizes[party]):
            ballots.append([f"({party}) {c}" for c in shuffled(parties[party])])

    print(f"Voters in each party: {party_sizes}")
    print(f"Resulting seats: {stv(5, ballots)}")