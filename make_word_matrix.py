import pandas as pd
from itertools import permutations

df = pd.read_csv("word.csv", header=0)
data = df["word"]

results = list(permutations(data, 2))
for word1, word2 in results:
    print(f"{word1}の{word2}")

