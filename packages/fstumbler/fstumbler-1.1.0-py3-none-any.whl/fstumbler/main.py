from time import perf_counter_ns

from core import tumble, tree, special_tree
from node import Node


t_0 = perf_counter_ns()
r = tumble('/home/ferit/scripts')
t_1 = perf_counter_ns()

print('Elapsed time: ', (t_1 - t_0) / 10 ** 9, ' seconds')

if r:
    t_0 = perf_counter_ns()
    count = r.ll_count()
    t_1 = perf_counter_ns()
    print('Elapsed time: ', (t_1 - t_0) / 10 ** 9, ' seconds')
    print(count, ' elements')

if r:
    #tree(r)
    print('='*10)
    special_tree(r, ['.git'], 4)
