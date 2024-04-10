"""
__author__ = "Ashwinkumar Ajithkumar Pillai"
__date__ = 3/12/24
__version__ = "1.0"
__license__ = "MIT style license file"
"""

import numpy as np

def hungarian(C: list, print_results:bool =False) -> tuple:

    """
    The hungarian function takes in the cost matrix and returns a tuple (job, acost) 
    where job is the list of TAs and acost is a list of cost is an numpy.ndarray 
    that stores the cost of assigning the TAs to the courses.

    Arguments
    ----------
    C : list
        the cost matrix
    print_results : bool
        flag to check if the user wants to print the results of hungarian assignments
        
    Returned Values
    ----------
    job, acost : tuple

    """

    J = len(C)
    W = len(C[0])
    assert J <= W
    job = [-1] * (W + 1)
    ys = [0] * J
    yt = [0] * (W + 1)
    answers = []
    acost = np.zeros(J)
    inf = float('inf')

    for j_cur in range(J):
        w_cur = W
        job[w_cur] = j_cur
        min_to = [inf] * (W + 1)
        prv = [-1] * (W + 1)
        in_Z = [False] * (W + 1)

        while job[w_cur] != -1:
            in_Z[w_cur] = True
            j = job[w_cur]
            delta = inf
            w_next = -1

            for w in range(W):
                if not in_Z[w]:
                    if C[j][w] - ys[j] - yt[w] < min_to[w]:
                        min_to[w] = C[j][w] - ys[j] - yt[w]
                        prv[w] = w_cur
                    if min_to[w] < delta:
                        delta = min_to[w]
                        w_next = w

            for w in range(W + 1):
                if in_Z[w]:
                    ys[job[w]] += delta
                    yt[w] -= delta
                else:
                    min_to[w] -= delta

            w_cur = w_next

        while w_cur != -1:
            w = prv[w_cur]
            job[w_cur] = job[w]
            w_cur = w

        answers.append(-yt[W])
        acost[j_cur] = -yt[W]

    if print_results:
        
        for w in range(len(job)-1):
            cost_string = ""
            if job[w] != -1:
                cost_string = str(C[job[w]][w])
            else:
                cost_string = "NA"
            print(f"({job[w]},{w}) -> Worker {job[w]} assigned to job {w} at cost: {cost_string}")

    return job, acost