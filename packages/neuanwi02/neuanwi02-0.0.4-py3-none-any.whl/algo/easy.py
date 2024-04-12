import heapq
from bisect import bisect_left, bisect_right

def heapsort(iterable):
    h = []
    result = []
    for value in iterable:
   	heapq.heappush(h, value)
    for i in range(len(h)):
       result.append(heapq.heappop(h))
    return result
