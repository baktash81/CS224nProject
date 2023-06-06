import os
import pandas as pd
import pickle
from collections import defaultdict
import matplotlib.pyplot as plt



if not os.path.exists("./stats"):
    print("make stats folder")
    os.makedirs("./stats")

# 10 non-common words of each label :

# load data and unique data of each label : 

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
  top_10 = sorted_items[:10]

  keys = []
  values = []

  for tup in top_10:
      keys.append(tup[0])
      values.append(tup[1])

  plt.plot(keys, values, 'bo')

  plt.xlabel('Words')
  plt.ylabel('Count')
  plt.title(f'Top_10_label_{label}_words')

  plt.xticks(rotation=45)  # Rotate x-axis tick labels by 45 degrees

  plt.savefig(f'./stats/Top_10_label_{label}_words.png')  # Save the plot as a PNG file
  # Show the plot
  plt.show()

  print()

