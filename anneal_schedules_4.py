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

def pause_schedule(p_length=20, s_start=0.5):
    return [ [0.0, 0.0], [10.0, s_start], [10.0+p_length, s_start], [20.0+p_length, 1.0] ]

# Pause grid search
p_vals = [10, 20, 30, 40, 50]
s_vals = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
df = pd.DataFrame(columns=["P", "S", "Chosen"])

for p in p_vals:
    for s in s_vals:
        print("\nPause length:", p, "\tPause start:", s)

        schedule = pause_schedule(p_length=p, s_start=s)

        sampler = FixedEmbeddingComposite(DWaveSampler(solver='Advantage_system4.1'), embedding=embedding)
        sampleset = sampler.sample(bqm, num_reads=1000, anneal_schedule=schedule)

        print("Best sample energy:", sampleset.first.energy)

        print("Number chosen:", sum(sampleset.first.sample.values()))

        df = df.append({"P": p, "S": s, "Chosen": sum(sampleset.first.sample.values())}, ignore_index=True)

df = df.pivot("P", "S", "Chosen")

fig, ax = plt.subplots()
ax = sns.heatmap(df, annot=True)
filename = "pause_schedule.png"
plt.savefig(filename, bbox_inches='tight')
