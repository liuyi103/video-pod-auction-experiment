"""
Created on Sat Aug 08 22:31:09 2015

@author: lyc
"""

from basic_functions import *

if __name__ == '__main__':
    max_duration = 45
    ads = data_sampler(100)
    winners = set(select_winners(ads, max_duration))
    losers = set(ads) - winners
    bar = [i[1] for i in get_coutour(losers, max_duration, True)]
    constraints = {}

    print len(winners)
    print bar
    for winner in winners:
        print winner.bid, winner.duration

    for winner in winners:
        constraints[(winner,)] = bar[winner['duration']]
    while True:
        print len(constraints)
        raw_input()
        get_solution(winners, constraints)
        lower_coutour = get_coutour(winners, max_duration, False)
        finish = True
        for k, tmp in enumerate(lower_coutour):
            ads, min_value = tmp
            if len(ads) == 0:
                continue
            if min_value < bar[k] - 1e-5:
                print min_value, bar[k]
                constraints[tuple(ads)] = bar[k]
                finish = False
        if finish:
            break
    for winner in winners:
        print winner.price