import os
import pandas as pd
import pickle
import matplotlib.pyplot as plt

def generalPlot(data, name) :


  x_labels = [ "NC-17", "PG-13", "G", "R", "PG", "All"]
  y_values = data

  plt.figure(figsize=(10, 6))
  plt.bar(x_labels, y_values, color='blue')
  plt.xlabel("Features")
  plt.ylabel("Counts")
  plt.title(name)

  plt.savefig(f'./stats/{name}.png')  # Save the plot as a PNG file
  plt.show()
  print()


def isUnique(word, label, withoutDuplicate) :
  # check if word of a label is unique or not
  for iterLabel in ['G', 'NC-17', 'PG', 'PG-13', 'R'] :
    if iterLabel == label :
      continue
    if word in withoutDuplicate[iterLabel] :
      return False
  return True


LANGUAGE = "eng"

if not os.path.exists("./stats"):
    print("make stats folder")
    os.makedirs("./stats")

# number of subtitle for each label :
subtitleLabels = {'G' : 0, 'NC-17' : 0, 'PG' : 0, 'PG-13' : 0, 'R' : 0}

# dict for data of each label : 
labelsDict = {'G' : [[],[]], 'NC-17' : [[],[]], 'PG' : [[],[]], 'PG-13' : [[],[]], 'R' : [[],[]]} # [[words], [sentences]]

# dict for unique data of each label : 
uniqueLabelsDict = {'G' : set(), 'NC-17' : set(), 'PG' : set(), 'PG-13' : set(), 'R' : set()}


# import labels :
labelDict = dict()
if os.path.exists("./data/clean/labels.txt") :
  with open("./data/clean/labels.txt", 'r') as labelFile :
    for line in labelFile :
      line = line.split()
      subtitleLabels[line[1]] += 1



# General Report : 


# import sentence data frame
sentenceDf = pd.read_csv('./data/sentencebroken/data.csv')

# import word data frame
wordDf = pd.read_csv('./data/wordbroken/data.csv')

# number of data (subtitle) : 
dataNum = sentenceDf.shape[0]

# number of sentences  :
sentenceDf['sentences'] = sentenceDf['sentences'].apply(lambda x: eval(x))
sentNum = sentenceDf['sentences'].apply(len).sum()


# number of all words :
wordDf['words'] = wordDf['words'].apply(lambda x: eval(x))
wordNum = wordDf['words'].apply(len).sum()


# number of all unique words :
uniqueWords = set()

for row in wordDf['words']:
    uniqueWords.update(row)

uniqueWordNum = len(uniqueWords)

# fill all words and sentences for each label
withoutDuplicate = {'G' : set(), 'NC-17' : set(), 'PG' : set(), 'PG-13' : set(), 'R' : set()}
for index, row in sentenceDf.iterrows():
  labelsDict[row["label"]][1].extend(row["sentences"])
  
for index, row in wordDf.iterrows():
  labelsDict[row["label"]][0].extend(row["words"])
  withoutDuplicate[row["label"]].update(row["words"])


# fill unique word of all label
for label in ["PG", "R", "G", "PG-13", "NC-17"] :
  wordList = list(withoutDuplicate[label])
  for word in  wordList :
    if isUnique(word, label, withoutDuplicate) :
      uniqueLabelsDict[label].add(word)

rows = [["All", dataNum, sentNum, wordNum, uniqueWordNum]]

for label in ["PG", "R", "G", "PG-13", "NC-17"] :
  labelRow = [label]

  # number of data (subtitle) : 
  labelRow.append(subtitleLabels[label])

  # number of sentences  :
  labelRow.append(len(labelsDict[label][1]))


  # number of all words :
  labelRow.append(len(labelsDict[label][0]))

  # number of all unique words :
  labelRow.append(len(withoutDuplicate[label]))

  rows.insert(0,labelRow)


with open('./stats/label_data_dic.pickle', 'wb') as file :
  pickle.dump(labelsDict, file)
with open('./stats/all_unique_words.pickle', 'wb') as file :
  pickle.dump(uniqueWords, file)
with open('./stats/label_unique_data_dic.pickle', 'wb') as file :
  pickle.dump(uniqueLabelsDict, file)


generalDf = pd.DataFrame(rows, columns=['label','number of data', 'number of sentences', 'number of words', 'number of unique words'])
generalDf.to_csv('./stats/general_report.csv', index=False)

## plot for general report :
dataFig = []
nameFig = ['number_of_subtitles', 'number_of_sentences', 'number_of_words', 'number_of_unique_words']
for i in range(4) :
  row = []
  for item in rows :
    row.append(item[i+1])
  generalPlot(row, nameFig[i])
