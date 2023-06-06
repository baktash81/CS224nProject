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

# save non-duplicates words
nonDuplicated = {'G' : set(), 'NC-17' : set(), 'PG' : set(), 'PG-13' : set(), 'R' : set()}

# save number of each word in dictionary (for all words) and fill nonDuplicated
all_words_num = defaultdict(int)
for label in ["PG", "R", "G", "PG-13", "NC-17"] :
  nonDuplicated[label] = set(labelsDict[label][0])
  for word in labelsDict[label][0] :
    all_words_num[word] += 1

# save number of labels which word appears on they :
wordLabelNum = defaultdict(int)
for word in list(all_words_num.keys()) :
  for label in ["PG", "R", "G", "PG-13", "NC-17"] :
    if word in nonDuplicated[label] :
      wordLabelNum[word] += 1

for label in ["PG", "R", "G", "PG-13", "NC-17"] :
  # save number of each word in dictionary (for words in specific label)
  label_words_num = defaultdict(int)
  for word in labelsDict[label][0] :
    label_words_num[word] += 1
  
  # calculate tf and idf :
  tfIdf = {}

  

  for word in list(nonDuplicated[label]) :
    tf = float( label_words_num[word] ) / all_words_num[word]
    idf = math.log ( 5.0 / wordLabelNum[word] )
    tfIdf[word] = tf * idf

  

  sorted_items = sorted(tfIdf.items(), key=lambda x: x[1], reverse=True)

  top_10 = sorted_items[:10]

  keys = []
  values = []

  for tup in top_10:
      keys.append(tup[0])
      values.append(tup[1])
  
  plt.figure(figsize=(8,8))
  
  plt.plot(keys, values, 'bo')

  plt.xlabel('Words')
  plt.ylabel('TF/IDF')
  plt.title(f'Top_10_TF_IDF_{label}_words')

  plt.xticks(rotation=45)  # Rotate x-axis tick labels by 45 degrees

  plt.savefig(f'./stats/Top_10_TF_IDF_{label}_words.png')  # Save the plot as a PNG file
  # Show the plot
  plt.show()

  print()  
