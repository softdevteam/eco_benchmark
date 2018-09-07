#! /usr/bin/env python2.7

import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.preamble'] = [r'\usepackage[cm]{sfmath}']
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = 'cm'
import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial.polynomial import polyfit
import os

timings = []

with open("results.csv", "r") as f:
    for l in f.readlines():
        name, size, results = l.split(" ")
        results2 = [float(r) for r in results.split(",")]
        average = sum(results2) / len(results2) * 1000
        with open(name, "r") as f2:
            lines = len(f2.readlines())
        if len(results2) >= 1:
            timings.append((lines, average))

timings.sort()

x = []
y = []
for s in timings:
    x.append(s[0])
    y.append(s[1])

x = np.array(x)
y = np.array(y)

# Calculate best-fit
b,m = polyfit(x, y, 1)

plt.rc('text', usetex=True)
plt.rc('font', family='sans-serif')
fig, ax = plt.subplots(figsize=(8, 4))
plt.plot(x, b + m * x, '-', linewidth=3, color="#43BFC7")
plt.plot(x, y, 'ro', markersize=4, color="#2B3856")
ax.grid(linewidth=0.25)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_xlabel("Number of lines", labelpad=10)
ax.set_ylabel("Time in ms", labelpad=10)
plt.tight_layout()
plt.savefig("performance.pdf", format="pdf")
plt.show()
