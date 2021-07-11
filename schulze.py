from numpy import zeros, array


def winner(p: array) -> array:

    results = []
    for i in range(len(p)):
        true = True
        for j in range(len(p)):
            if i != j:
                true = p[i, j] >= p[j, i] and true
                if not true:
                    break
        if true:
            results.append(i)
    return results


def main(d: array) -> list:
    p = zeros((len(d), len(d)))
    for i in range(len(d)):
        for j in range(len(d)):
            if i != j:
                if d[i, j] > d[j, i]:
                    p[i, j] = d[i, j]
                else:
                    p[i, j] = 0

    for i in range(len(d)):
        for j in range(len(d)):
            if i != j:
                for k in range(len(d)):
                    if i != k and j != k:
                        p[j, k] = max(p[j, k], min(p[j, i], p[i, k]))
    return winner(p)
