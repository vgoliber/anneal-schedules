# ------ Import necessary packages ----

from collections import defaultdict

from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
from dimod import BQM

# choose exactly two BQM
n = 100

bqm = BQM('BINARY')

for i in range(n):
    bqm.add_linear(i, -3)
    for j in range(i+1,n):
        bqm.add_quadratic(i, j, 2)

bqm.offset = 4

sampler = EmbeddingComposite(DWaveSampler())
sampleset = sampler.sample(bqm, num_reads=1000)

print(sampleset)

print("\nNumber chosen:", sum(sampleset.first.sample.values()))
