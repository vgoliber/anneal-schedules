# ------ Import necessary packages ----

from collections import defaultdict
import json

from dwave.system.samplers import DWaveSampler
from dwave.system.composites import FixedEmbeddingComposite
from dimod import BQM

# choose exactly two BQM
n = 100

bqm = BQM('BINARY')

for i in range(n):
    bqm.add_linear(str(i), -3)
    for j in range(i+1,n):
        bqm.add_quadratic(str(i), str(j), 2)

bqm.offset = 4

# Retrieve precomputed embedding
embedding = {}
with open('embedding.json') as json_file:
     embedding = json.load(json_file)

def quench_schedule(q_start=10):

    standard_slope = 1/20

    return [ [0.0, 0.0], [q_start, q_start*standard_slope], [1-q_start*standard_slope+q_start, 1.0] ]

# Quench search
q_vals = [5, 10, 15, 18]

for q in q_vals:
    print("\nQuench start:", q)

    schedule = quench_schedule(q_start=q)
    print(schedule)

    sampler = FixedEmbeddingComposite(DWaveSampler(solver='Advantage_system4.1'), embedding=embedding)
    sampleset = sampler.sample(bqm, num_reads=1000, anneal_schedule=schedule)

    print("Best sample energy:", sampleset.first.energy)

    print("Number chosen:", sum(sampleset.first.sample.values()))
