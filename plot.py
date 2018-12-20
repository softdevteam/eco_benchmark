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

def load_results(name, limit_lines=None):
    timings = []
    with open(name, "r") as f:
        for l in f.readlines():
            name, size, results = l.split(" ")
            name = name.replace("lukasd/eco_benchmark", "lukas/research")
            results2 = [float(r) for r in results.split(",")]
            average = sum(results2) / len(results2) * 1000
            with open(name, "r") as f2:
                lines = len(f2.readlines())
            if limit_lines and lines > limit_lines:
                continue
            if len(results2) >= 1:
                timings.append((lines, average))
    return timings

def add_timings_to_plot(plt, filename, colour1, colour2, bestfit=False, limit=None):
    timings = load_results(filename, limit)
    timings.sort()
    x = []
    y = []
    for s in timings:
        x.append(s[0])
        y.append(s[1])
    x = np.array(x)
    y = np.array(y)
    if bestfit:
        # Calculate best-fit
        b,m = polyfit(x, y, 1)
        plt.plot(x, b + m * x, '-', linewidth=3, color=colour2)
    plt.plot(x, y, 'ro', markersize=4, color=colour1)

def plot(typ, output, bestfit=True, limit=None):
    plt.rc('text', usetex=True)
    plt.rc('font', family='sans-serif')
    fig, ax = plt.subplots(figsize=(8, 4))
    if typ == "traditional" or typ == "both":
        add_timings_to_plot(plt, "results_t.csv", "#B22222", "#00FF00", bestfit, limit)
    if typ == "incremental" or typ == "both":
        add_timings_to_plot(plt, "results.csv", "#2B3856", "#43BFC7", bestfit, limit)
    ax.legend(["Traditional parsing", "Incremental parsing"])
    ax.grid(linewidth=0.25)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_xlabel("Number of lines", labelpad=10)
    ax.set_ylabel("Time in ms", labelpad=10)
    plt.tight_layout()
    plt.savefig(output, format="pdf")

if __name__ == "__main__":
    #plot("incremental", "performance.pdf")
    #plot("traditional", "performance_t.pdf")
    plot("both", "performance_b.pdf", bestfit=False)
    #plot("both", "performance_bl.pdf", bestfit=False, limit=1000)
