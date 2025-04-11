# gale_shapley.py

def stable_matching(proposers, receivers, proposers_preferences, receivers_preferences):

    # Start with all proposers as free and no receiver engaged.
    free_proposers = set(proposers)
    current_matches = {}  # Maps each receiver to its current proposer.
    # Track which receivers each proposer has already proposed to.
    proposals = {p: [] for p in proposers}

    while free_proposers:
        # Pick an arbitrary free proposer
        p = free_proposers.pop()

        # Propose to the next receiver on p's list that they haven't proposed to yet.
        for r in proposers_preferences[p]:
            if r not in proposals[p]:
                proposals[p].append(r)
                # If the receiver is not yet engaged, accept the proposal.
                if r not in current_matches:
                    current_matches[r] = p
                    break
                else:
                    current_partner = current_matches[r]
                    # Compare preference indices. A lower index means a higher preference.
                    if receivers_preferences[r].index(p) < receivers_preferences[r].index(current_partner):
                        # The receiver prefers the new proposer over the current partner.
                        current_matches[r] = p
                        free_proposers.add(current_partner)
                        break
                    # If the receiver prefers its current match, p gets rejected.
                    else:
                        continue
        # (If a proposer has proposed to all receivers, they remain unmatched.)

    # Convert the mapping (receiver -> proposer) to (proposer -> receiver)
    matches = {v: k for k, v in current_matches.items()}
    return matches
