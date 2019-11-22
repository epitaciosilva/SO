import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
 
def func(data):
    if 'sequencial' in data:
        return "sequencial"
    return data

plt.figure(figsize=(20,10))
df = pd.read_csv('benchmark.csv')

grouped = df.groupby('n')
for name, group in grouped:
    # organiza os grupos
    group = group.sort_values(by=['algoritmo', 'threads'])
    group['nome'] = group['algoritmo'] + ": " + (group['threads'].map(str) + " " + group['tipo']).map(func)
    group = group.drop(columns=['algoritmo', 'tipo', 'threads'])
    
    xlabel = "Valor de N:" + group['n'].map(str).iloc[0]

    #formata o plot
    plt.xticks(fontsize=18, rotation=15)
    plt.yticks(fontsize=25)
    plt.ylabel("Tempo em segundos", fontsize=25)
    plt.title(xlabel, fontsize=25)
    plt.xlabel(xlabel, fontsize=25)
    plt.bar(group['nome'], group['tempo'], color=("#ff5733", "#a43720", "#a43720", "#a43720", "#C70039", "#C70039", "#C70039"), capsize=25)
    plt.savefig(xlabel)
