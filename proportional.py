import math

def highest_averages(divisor, num_seats, votes, guaranteed_min_seats=0, majority_check=True, super_check=True):
    result = {party: guaranteed_min_seats for party in votes}
    total_votes = sum(votes[party] for party in votes)
    seat_guarantee_quota = total_votes / num_seats

    # print(f"Quota: {seat_guarantee_quota}")

    # Majority and supermajority quotas
    majority_seats = math.floor(num_seats / 2) + 1
    majority_votes = math.floor(total_votes / 2) + 1

    super_seats = math.ceil(2 * num_seats / 3)
    super_votes = math.ceil(2 * total_votes / 3)
    for party in votes:
        # Calculate how many whole seats each party gets.
        result[party] = min(guaranteed_min_seats, math.floor(votes[party] / seat_guarantee_quota))
        num_seats -= result[party]
    
    # print(f"After quota-based apportionment, remaining seats={num_seats}, votes={result}")
    
    # Use divisor priority to fill remaining seats
    for n in range(num_seats):
        max_quotient, max_quotient_party = -1, None

        quotients = {}
        for party in votes:
            k = result[party] + 1

            if super_check and k >= super_seats and votes[party] < super_votes or \
                majority_check and k >= majority_seats and votes[party] < majority_votes:
                # A party may not have a [super]majority of seats unless it has a [super]majority of votes.
                # This party cannot receive any more seats.
                # print(f"[Super]majority rule: party={party}, majority_seats={majority_seats}, super_seats={super_seats}")
                votes[party] = 0 # Force quotient to 0

            quotient = votes[party]/divisor(k)
            quotients[party] = quotient
            if quotient > max_quotient:
                max_quotient, max_quotient_party = quotient, party

        result[max_quotient_party] += 1

        # print(f"round={n}, quotients={quotients}")
        # print(f"{n+1}/{num_seats} elected {max_quotient_party}")

    return result

def dhondt(num_seats, votes):
    return highest_averages(lambda k: k, num_seats, votes)

def piecewise_huntington_hill(num_seats, votes, **kwargs):
    return highest_averages(lambda k: k if k <= 1 else math.sqrt(k * (k - 1)), num_seats, votes, **kwargs)

def stv(num_seats, votes):
    weights = {}
    elected = set()

    while len(elected) < num_seats:
        transferring_surplus_votes = True
        counts = {}

        while transferring_surplus_votes:
            total_votes = 0
            excess = 0

            for ballot in votes:
                vote_remaining = 1

                for candidate in ballot:
                    if candidate not in weights:
                        weights[candidate] = 1 # Hopeful
                    
                    if candidate not in counts:
                        counts[candidate] = 0
                    
                    counts[candidate] += vote_remaining * weights[candidate]
                    vote_remaining *= 1 - weights[candidate]
                    if vote_remaining == 0:
                        break
                
                excess += vote_remaining

                total_votes += 1
            
            quota = (total_votes - excess) / (num_seats + 1)
            # print(f"quota={quota}, counts={counts}, weights={weights}, excess={excess}")

            transferring_surplus_votes = False
            if quota == 0:
                # All votes are going to excess; we can't elect any more seats.
                break

            for candidate in counts:
                if weights[candidate] == 0:
                    continue # Excluded

                if candidate not in elected and counts[candidate] >= quota:
                    elected.add(candidate)
                    # print(f"{len(elected)}/{num_seats} candidate {candidate} elected")


                if candidate in elected and abs(counts[candidate] - quota)/quota > .000001:
                    weights[candidate] *= quota/counts[candidate]
                    transferring_surplus_votes = True
            
            if transferring_surplus_votes:
                counts = {}

        # Eliminate the Hopeful candidate with the lowest count
        can_be_eliminated_candidates = list((candidate, counts[candidate]) for candidate in counts if candidate not in elected and weights[candidate] > 0)
        if len(can_be_eliminated_candidates) > 0:
            lowest_candidate, _ = min(can_be_eliminated_candidates, key=lambda x: x[1])
            # print(f"{lowest_candidate} eliminated")
            weights[lowest_candidate] = 0
            counts = {}
            excess = 0
        else:
            # print(f"No candidates can be eliminated; counts={counts}")
            break
    
    return list(elected)
