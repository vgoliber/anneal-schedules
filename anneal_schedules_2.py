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

sampler = FixedEmbeddingComposite(DWaveSampler(solver='Advantage_system4.1'), embedding=embedding)
sampleset = sampler.sample(bqm, num_reads=1000)

print(sampleset)

print("\nNumber chosen:", sum(sampleset.first.sample.values()))
