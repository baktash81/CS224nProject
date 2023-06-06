import os
import pandas as pd
import pickle
from collections import defaultdict
import matplotlib.pyplot as plt
import math

if not os.path.exists("./stats"):
    print("make stats folder")
    os.makedirs("./stats")

# load data of each label : 
labelsDict = {}
with open('./stats/label_data_dic.pickle', 'rb') as file :
  labelsDict = pickle.load(file)
  

uniqueLabelsDict = {}
with open('./stats/label_unique_data_dic.pickle', 'rb') as file :
  uniqueLabelsDict = pickle.load(file)

for label in ["PG", "R", "G", "PG-13", "NC-17"] :
  # save number of each word in dictionary
  words_num = defaultdict(int)
  for word in labelsDict[label][0] :
    words_num[word] += 1

  # dict for each word and number of frequency 
  label_frequency = {}
  for word in uniqueLabelsDict[label] :
    label_frequency[word] = words_num[word]
  
  sorted_items = sorted(label_frequency.items(), key=lambda x: x[1], reverse=True)
  top_15 = sorted_items[:15]

  hitData = []
  for key, value in top_15 :
    for i in range(value) :
      hitData.append(key)

  plt.figure(figsize=(8,8))
  
  plt.xlabel('Words')
  plt.ylabel('Count')
  plt.title(f'Top_15_Freq__Histogram_{label}_words')

  plt.hist(hitData)

  plt.xticks(rotation=45)

  plt.savefig(f'./stats/Top_15_Freq__Histogram_{label}_Words.png')  # Save the plot as a PNG file

  plt.show()

  print()


  
