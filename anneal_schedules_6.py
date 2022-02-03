# ------ Import necessary packages ----

from collections import defaultdict
import json

from dwave.system.samplers import DWaveSampler
from dwave.system.composites import FixedEmbeddingComposite
from dimod import BQM

import seaborn as sns
import pandas as pd

import matplotlib
matplotlib.use("agg")
from matplotlib import pyplot as plt

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

def pq_schedule(q_start=10, p_length=10):

    standard_slope = 1/20

    return [ [0.0, 0.0], [q_start, q_start*standard_slope], [q_start+p_length, q_start*standard_slope], [1-q_start*standard_slope+q_start+p_length, 1.0] ]

# Quench+pause search
q_vals = [5, 10, 15, 18]
p_vals = [10, 20, 30, 40, 50]
df = pd.DataFrame(columns=["Q", "P", "Chosen"])

for q in q_vals:
    for p in p_vals:
        print("\nQuench start:", q, "\tPause length:", p)

        schedule = pq_schedule(q_start=q, p_length=p)
        print(schedule)

        sampler = FixedEmbeddingComposite(DWaveSampler(solver='Advantage_system4.1'), embedding=embedding)
        sampleset = sampler.sample(bqm, num_reads=1000, anneal_schedule=schedule)

        print("Best sample energy:", sampleset.first.energy)

        print("Number chosen:", sum(sampleset.first.sample.values()))

        df = df.append({"P": p, "Q": q, "Chosen": sum(sampleset.first.sample.values())}, ignore_index=True)

df = df.pivot("P", "Q", "Chosen")
df = df.astype(float)
print(df)

fig, ax = plt.subplots()
ax = sns.heatmap(df, annot=True)
filename = "pause_quench_schedule.png"
plt.savefig(filename, bbox_inches='tight')
