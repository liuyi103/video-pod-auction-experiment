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
    # for i, x in enumerate(winners):
    #     ceil = 1e9
    #     for k, y in enumerate(winners[i+1:]):
    #         j = i + 1 + k
    #         if y.bid == x.bid:
    #             if x.duration == y.duration:
    #                 prob.linear_constraints.add([[[i, j], [1,-1]]], ['E'], [0])
    #             else:
    #                 prob.linear_constraints.add([[[i, j],[1,-1]]],['L'],[0])
    #             break
    #         if y.bid > x.bid and y.bid < ceil:
    #             ceil = y.bid
    #             prob.linear_constraints.add([[[i,j],[1,-1]]],['L'],[0])

    n_iteration = 0
    last_obj = -1
    while True:
        n_iteration += 1
        prob.solve()
        obj = prob.solution.get_objective_value()
        last_obj = obj
        prices = prob.solution.get_values()
        for i, winner in enumerate(winners):
            winner.price = prices[i]
        lower_coutour = get_coutour(winners, max_duration, False)
        finish = True
        for k, tmp in enumerate(lower_coutour):
            ads, min_value = tmp
            if len(ads) == 0:
                continue
            if min_value < bar[k] - 1e-4:
                prob.linear_constraints.add([[[id2num[id(ad)] for ad in ads], [1] * len(ads)]],\
                    ['G'], [bar[k]])
                finish = False
        if finish:
            break
    return sum(prob.solution.get_values()), len(winners), n_iteration

# def solveit2(max_duration, ads):
#     '''
#     add only 1 constraint each iteration
#     :param max_duration:
#     :param ads:
#     :return:
#     '''
#     # get the winners
#     winners, losers = select_winners(ads, max_duration)
#     llosers = list(losers)
#     # add a fake winner if needed.
#     total_dur = sum([winner.duration for winner in winners])
#     if total_dur < max_duration:
#         winners.add(Ad(bid = 0, duration =max_duration - total_dur))
#
#     # get the upper contour for the losers
#     bar = [i[1] for i in get_coutour(losers, max_duration, True)]
#
#     winners = sorted(winners, key = lambda winner: (winner.duration, winner.bid))
#     id2num = {id(winner):k for k, winner in enumerate(winners)}
#     prob = Cplex()
#     lb = [bar[winner.duration] for winner in winners]
#     ub = [winner.bid for winner in winners]
#     prob.objective.set_sense(prob.objective.sense.minimize)
#     obj = [1] * len(winners)
#     prob.variables.add(obj, lb, ub)
#
#     # monotone requirement (optional)
#     # for i, x in enumerate(winners):
#     #     ceil = 1e9
#     #     for k, y in enumerate(winners[i+1:]):
#     #         j = i + 1 + k
#     #         if y.bid == x.bid:
#     #             if x.duration == y.duration:
#     #                 prob.linear_constraints.add([[[i, j], [1,-1]]], ['E'], [0])
#     #             else:
#     #                 prob.linear_constraints.add([[[i, j],[1,-1]]],['L'],[0])
#     #             break
#     #         if y.bid > x.bid and y.bid < ceil:
#     #             ceil = y.bid
#     #             prob.linear_constraints.add([[[i,j],[1,-1]]],['L'],[0])
#
#     n_iteration = 0
#     while True:
#         n_iteration += 1
#         prob.solve()
#         prices = prob.solution.get_values()
#         fake_winners = [Ad(bid=prices[k], duration=winner.duration) for k,winner in enumerate(winners)]
#         tmp_winners, _ = select_winners(fake_winners+llosers, max_duration)
#         sum1 = sum([winner['bid'] for winner in tmp_winners])
#         sum2 = sum([winner['bid'] for winner in fake_winners])
#         if sum1 > sum2 + 1e-5:
#             c = sum1 - sum2
#             ind = []
#             for k, winner in enumerate(fake_winners):
#                 if winner not in tmp_winners:
#                     ind.append(k)
#                     c += winner['price']
#             prob.linear_constraints.add([[ind, [1]*len(ind)]], 'G', [c])
#         else:
#             break
#     return sum(prob.solution.get_values()), len(winners), n_iteration

if __name__ == '__main__':
    n_iters = []
    times = []
    for i in range(100):
        max_duration = 500
        ads = data_sampler(200)
        f = file('data.txt', 'w')
        for ad in ads:
            f.write('%lf %lf\n'%(ad['bid'], ad['duration']))
        st_time = time.time()
        revenue, n_winners, n_iter = solveit(max_duration, ads)
        en_time = time.time()
        n_iters.append(n_iter)
        times.append(en_time - st_time)
        print revenue, n_winners
    print n_iters, times
    # max_duration = 500
    # ads = []
    # f = file('data.txt', 'r')
    # for line in f:
    #     bid, duration = line.split()
    #     bid, duration = float(bid), int(float(duration))
    #     ads.append(Ad(bid = bid, duration=duration))
    # solveit(max_duration, ads)


