#!/usr/bin/env python

import collections, math, sys, json, os

def main():
    mu = float(os.environ['MU']) if os.environ.has_key('MU') else 0.002
    eta = float(os.environ['ETA']) if os.environ.has_key('ETA') else 0.5
    T = int(os.environ['T']) if os.environ.has_key('T') else 1
    split = float(os.environ['SPLIT']) if os.environ.has_key('SPLIT') else 0.3
    n_models_key = os.environ['N_MODELS_KEY'] if os.environ.has_key('N_MODELS_KEY') else 'MODEL'
    k = 0
    W = collections.defaultdict(float)
    A = collections.defaultdict(int)
    lines = [ line for line in sys.stdin ]
    for t in range(1, T+1):
        for line in lines:
            x = json.loads(line)
            if x.has_key('class') and x["random_key"] > split:
                sigma = sum([W[j] * x["features"][j] for j in x["features"].keys()])
                p = 1. / (1. + math.exp(-sigma)) if -100. < sigma else sys.float_info.min
                k += 1
                lambd4 = eta / float(pow(t, 2))
                penalty = 1. - (2. * lambd4 * mu)
                for j in x["features"].keys():
                    W[j] *= math.pow(penalty, k - A[j])
                    W[j] += lambd4 * (float(x["class"]) - p) * x["features"][j]
                    A[j] = k
    lambd4 = eta / float(pow(T, 2))
    penalty = 1. - (2. * lambd4 * mu)
    print "%s\t%17.16f" % (n_models_key, 1.)
    for j in W.keys():
        W[j] *= math.pow(penalty, k - A[j])
        print "%s\t%17.16f" % (j, W[j])
    
if __name__ == '__main__':
    main()
