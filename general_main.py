"""
Created on Sat Aug 08 22:31:09 2015

@author: lyc
"""

from basic_functions import *
from cplex import Cplex
import time

def solveit(max_duration, ads):
    # get the winners
    winners, losers = select_winners(ads, max_duration)

    # add a fake winner if needed.
    total_dur = sum([winner.duration for winner in winners])
    if total_dur < max_duration:
        winners.add(Ad(bid = 0, duration =max_duration - total_dur))

    # get the upper contour for the losers
    bar = [i[1] for i in get_coutour(losers, max_duration, True)]

    winners = sorted(winners, key = lambda winner: (winner.duration, winner.bid))
    id2num = {id(winner):k for k, winner in enumerate(winners)}
    prob = Cplex()
    lb = [bar[winner.duration] for winner in winners]
    ub = [winner.bid for winner in winners]
    prob.objective.set_sense(prob.objective.sense.minimize)
    obj = [1] * len(winners)
    prob.variables.add(obj, lb, ub)

    # monotone requirement (optional)
    for i, x in enumerate(winners):
        ceil = 1e9
        for k, y in enumerate(winners[i+1:]):
            j = i + 1 + k
            if y.bid == x.bid:
                if x.duration == y.duration:
                    prob.linear_constraints.add([[[i, j], [1,-1]]], ['E'], [0])
                else:
                    prob.linear_constraints.add([[[i, j],[1,-1]]],['L'],[0])
                break
            if y.bid > x.bid and y.bid < ceil:
                ceil = y.bid
                prob.linear_constraints.add([[[i,j],[1,-1]]],['L'],[0])

    n_iteration = 0
    while True:
        n_iteration += 1
        prob.solve()
        prices = prob.solution.get_values()
        print len(prices), len(winners)
        for i, winner in enumerate(winners):
            winner.price = prices[i]
        lower_coutour = get_coutour(winners, max_duration, False)
        finish = True
        for k, tmp in enumerate(lower_coutour):
            ads, min_value = tmp
            if len(ads) == 0:
                continue
            if min_value < bar[k] - 1e-5:
                prob.linear_constraints.add([[[id2num[id(ad)] for ad in ads],[1] * len(ads)]],\
                    ['G'], [bar[k]])
                finish = False
        if finish:
            break
    return sum(prob.solution.get_values()), len(winners), n_iteration


if __name__ == '__main__':
    n_iters = []
    times = []
    for i in range(10):
        max_duration = 200
        ads = data_sampler(50)
        st_time = time.time()
        revenue, n_winners, n_iter = solveit(max_duration, ads)
        en_time = time.time()
        n_iters.append(n_iter)
        times.append(en_time - st_time)
        print revenue, n_winners
    print n_iters, times
