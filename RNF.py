import os
import pandas as pd
import pickle
from collections import defaultdict
import matplotlib.pyplot as plt

if not os.path.exists("./stats"):
    print("make stats folder")
    os.makedirs("./stats")

# load data  of each label : 
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


# save number of each word of each label
labelCountWords = {'G' : {}, 'NC-17' : {}, 'PG' : {}, 'PG-13' : {}, 'R' : {}}

for label in ["PG", "R", "G", "PG-13", "NC-17"] :
  # save number of each word in dictionary (for words in specific label)
  label_words_num = defaultdict(int)
  for word in labelsDict[label][0] :
    label_words_num[word] += 1
  labelCountWords[label] = label_words_num

labels = ["PG", "R", "G", "PG-13", "NC-17"]

for i in range(5) :
  for j in range(i + 1, 5) :

    # save words that they are common in 2 labels :
    commonWords = set()
    for word in all_words_num.keys() :
      if (word in nonDuplicated[labels[i]]) and (word in nonDuplicated[labels[j]]) :
        commonWords.add(word)

    # for i_j label
    # dictionary for save RNF of each word for this label
    rnfDic = {}
    for word in commonWords :
      RNF =  ( float(labelCountWords[labels[i]][word]) / len(labelsDict[labels[i]][0]) ) / ( float(labelCountWords[labels[j]][word]) / len(labelsDict[labels[j]][0]) )
      rnfDic[word] = RNF

    sorted_items = sorted(rnfDic.items(), key=lambda x: x[1], reverse=True)
    top_10 = sorted_items[:10]

    keys = []
    values = []

    for tup in top_10:
        keys.append(tup[0])
        values.append(tup[1])

    plt.plot(keys, values, 'bo')

    plt.xlabel('Words')
    plt.ylabel('Count')
    plt.title(f'Top_10_common_RNF_{labels[i]}_{labels[j]}_words')

    plt.xticks(rotation=45)  # Rotate x-axis tick labels by 45 degrees

    plt.savefig(f'./stats/Top_10_common_RNF_{labels[i]}_{labels[j]}_words.png')  # Save the plot as a PNG file
    # Show the plot
    plt.show()

    print()

    # for j_i label
    # dictionary for save RNF of each word for this label
    rnfDic = {}
    for word in commonWords :
      RNF =  ( float(labelCountWords[labels[j]][word]) / len(labelsDict[labels[j]][0]) ) / ( float(labelCountWords[labels[i]][word]) / len(labelsDict[labels[i]][0]) )
      rnfDic[word] = RNF

    sorted_items = sorted(rnfDic.items(), key=lambda x: x[1], reverse=True)
    top_10 = sorted_items[:10]

    keys = []
    values = []

    for tup in top_10:
        keys.append(tup[0])
        values.append(tup[1])

    plt.plot(keys, values, 'bo')

    plt.xlabel('Words')
    plt.ylabel('Count')
    plt.title(f'Top_10_common_RNF_{labels[j]}_{labels[i]}_words')

    plt.xticks(rotation=45)  # Rotate x-axis tick labels by 45 degrees

    plt.savefig(f'./stats/Top_10_common_RNF_{labels[j]}_{labels[i]}_words.png')  # Save the plot as a PNG file
    # Show the plot
    plt.show()

    print()
  
