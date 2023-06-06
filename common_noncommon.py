import os
import pandas as pd
import pickle


labels = ["PG", "R", "G", "PG-13", "NC-17"]

if not os.path.exists("./stats"):
    print("make stats folder")
    os.makedirs("./stats")

# load data of each label : 
labelsDict = {}
with open('./stats/label_data_dic.pickle', 'rb') as file :
  labelsDict = pickle.load(file)


common_Df_list = []
non_common_Df_list = []
for i in range(5) :
  for j in range(i + 1, 5) :

    commonWordCount = set()
    nonCommonWordCount = set()
    label = f'{labels[i]}/{labels[j]}'
    firstSet = set(labelsDict[labels[i]][0])
    seccondSet = set(labelsDict[labels[j]][0])

    # for i-j label
    for word in firstSet : 
      if word in seccondSet :
        commonWordCount.add(word)
      else :
        nonCommonWordCount.add(word)

    number_of_common_words = len(commonWordCount)
    number_of_non_common_words = len(nonCommonWordCount)

    common_Df_list.append([label, number_of_common_words])
    non_common_Df_list.append([label, number_of_non_common_words])

    commonWordCount = set()
    nonCommonWordCount = set()
    label = f'{labels[j]}/{labels[i]}'
    # for j-i label
    for word in seccondSet : 
      if word in firstSet :
        commonWordCount.add(word)
      else :
        nonCommonWordCount.add(word)

    number_of_common_words = len(commonWordCount)
    number_of_non_common_words = len(nonCommonWordCount)

    common_Df_list.append([label, number_of_common_words])
    non_common_Df_list.append([label, number_of_non_common_words])

common_Df = pd.DataFrame(common_Df_list, columns=['Labels', "Number of common tokens"])
common_Df.to_csv('./stats/commonTokens.csv', index=False)

non_common_Df = pd.DataFrame(non_common_Df_list, columns=['Labels', "Number of non-common tokens"])
non_common_Df.to_csv('./stats/noncommonTokens.csv', index=False)
print(common_Df)
print(non_common_Df)