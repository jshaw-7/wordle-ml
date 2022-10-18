import numpy as np 
import pandas as pd 

import os

from pyod.models.copod import COPOD
import random
import matplotlib.pyplot as plt
import seaborn as sns
import string
import re
from collections import Counter
import colorama
from colorama import Fore


with open('wordle-allowed-guesses.txt', 'r') as f:
    allowed = f.read().splitlines()
with open('wordle-answers-alphabetical.txt','r') as f:
    answers = f.read().splitlines()
allowed += answers

letters = []
for word in answers:
    for letter in word:
        letters.append(letter)

count = Counter(letters)

answers_letter_frequency = pd.DataFrame.from_dict(count, orient='index').sort_values(0, ascending = False)
answers_letter_frequency.rename(columns = {0:'answer letter frequency',}, inplace = True)
answers_letter_frequency.plot(kind='bar',figsize=(10,3))


letters = []
for word in allowed:
    for letter in word:
        letters.append(letter)

count = Counter(letters)

allowed_letter_frequency = pd.DataFrame.from_dict(count, orient='index').sort_values(0, ascending = False)
allowed_letter_frequency.rename(columns = {0:'allowed letter frequency',}, inplace = True)
allowed_letter_frequency.plot(kind='bar',figsize=(10,3))

letters = ['a1', 'a2', 'a3', 'a4', 'a5', 'b1', 'b2', 'b3', 'b4', 'b5', 'c1', 'c2', 'c3', 'c4', 'c5', 
          'd1', 'd2', 'd3', 'd4', 'd5', 'e1', 'e2', 'e3', 'e4', 'e5', 'f1', 'f2', 'f3', 'f4', 'f5', 
           'g1', 'g2', 'g3', 'g4', 'g5', 'h1', 'h2', 'h3', 'h4', 'h5', 'i1', 'i2', 'i3', 'i4', 'i5',
           'j1', 'j2', 'j3', 'j4', 'j5', 'k1', 'k2', 'k3', 'k4', 'k5', 'l1', 'l2', 'l3', 'l4', 'l5', 
           'm1', 'm2', 'm3', 'm4', 'm5', 'n1', 'n2', 'n3', 'n4', 'n5', 'o1', 'o2', 'o3', 'o4', 'o5', 
           'p1', 'p2', 'p3', 'p4', 'p5', 'q1', 'q2', 'q3', 'q4', 'q5', 'r1', 'r2', 'r3', 'r4', 'r5', 
           's1', 's2', 's3', 's4', 's5', 't1', 't2', 't3', 't4', 't5', 'u1', 'u2', 'u3', 'u4', 'u5', 
           'v1', 'v2', 'v3', 'v4', 'v5', 'w1', 'w2', 'w3', 'w4', 'w5', 'x1', 'x2', 'x3', 'x4', 'x5',
           'y1', 'y2', 'y3', 'y4', 'y5', 'z1', 'z2', 'z3', 'z4', 'z5']

positions = []
for word in allowed:
    tmp = []
    for i in range(130):
        tmp.append(0)
    for i in range(4):
        letter = ord(word[i]) - 97
        tmp[(letter*5) + i] = 1
    positions.append(tmp)
allowed_letter_positions = pd.DataFrame(positions, index = [allowed], columns = letters)

positions = []
for word in answers:
    tmp = []
    for i in range(130):
        tmp.append(0)
    for i in range(4):
        letter = ord(word[i]) - 97
        tmp[(letter*5) + i] = 1
    positions.append(tmp)
answers_letter_positions = pd.DataFrame(positions, index = [answers], columns = letters)

answers_letter_positions.head()

answers_letter_positions['total_rank'] = 0

copod_model = COPOD()
copod_model.fit(answers_letter_positions)

answers_letter_positions['score'] = copod_model.decision_scores_
answers_letter_positions.sort_values('score',inplace=True)
answers_letter_positions['rank'] = range(1,len(answers_letter_positions)+1)
answers_letter_positions['total_rank'] += answers_letter_positions['rank']

answers_letter_positions.sort_values('total_rank',inplace=True)
answers_letter_positions['rank'] = range(1,len(answers_letter_positions)+1)
letters.append('total_rank')
answers_letter_positions.drop(columns = letters, inplace = True)
print(answers_letter_positions.head(20))