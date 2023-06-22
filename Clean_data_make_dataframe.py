import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import pickle
import os
import pandas as pd
from sklearn.model_selection import train_test_split


def clean_subtitle(subtitle):
    # Remove time stamps
    subtitle = re.sub(r'\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+\n', '', subtitle)
    
    # Remove HTML tags
    subtitle = re.sub(r'<.*?>', '', subtitle)
    
    # Remove URLs
    subtitle = re.sub(r'http\S+|www\S+', '', subtitle)

    # Remove sequence numbers    

    subtitle = subtitle.split('\n')
    subList = []

    for line in subtitle :

      if  line.isdigit() :
        continue
      subList.append(line)

    subtitle = '\n'.join(subList)
    
    # Remove non-text characters
    subtitle = re.sub(r'[^\w\s]', ' ', subtitle)
    
    # Remove empty lines
    subtitle = '\n'.join(line for line in subtitle.split('\n') if line.strip())

    # lower :
    subtitle = subtitle.lower()

    subList = subtitle.split('\n')


    # remove first n lines of start and end 
    n = 3 
    subList = subList[n :]
    subList = subList[ : -n - 2]

    final_sentences = []

    for sentence in subList : 
      if sentence == '' : 
        continue
      final_sentences.append(sentence)

    # Create a translation table using the string module
    translator = str.maketrans('', '', string.punctuation)
    
    # Remove punctuation from each sentence in the list
    final_sentences = [sentence.translate(translator) for sentence in final_sentences]
    

    # sentences = sent_tokenize(subtitle)

    # for i in range(len(sentences)) :
    #   sentences[i] = sentences[i].replace('\n', ' ')
    #   sentences[i] = sentences[i].strip()
    #   # split into words
    #   tokens = word_tokenize(sentences[i])

    #   # convert to lower case
    #   tokens = [w.lower() for w in tokens]

    #   # remove punctuation from each word
    #   table = str.maketrans('', '', string.punctuation)
    #   stripped = [w.translate(table) for w in tokens]

    #   # remove remaining tokens that are not alphabetic
    #   words = [word for word in stripped if word.isalpha()]

    #   # filter out stop words
      
    #   stop_words = set(stopwords.words('english'))
    #   words = [w for w in words if not w in stop_words]

    #   sentences[i] = " ".join(words)

    # final_sentences = []

    # for sentence in sentences : 
    #   if sentence == '' : 
    #     continue
    #   final_sentences.append(sentence)

    sentences = '\n'.join(final_sentences)

    return sentences

def sentence2word(sentences) :
  words = []
  for sentence in sentences :
    tokens = word_tokenize(sentence)
    words.extend(tokens)
  return words


LANGUAGE = "eng"

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Cleaning Data ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`")

files = os.listdir(f"./data/raw/subtitles/{LANGUAGE}")
cleanedFiles = os.listdir(f"./data/clean/subtitles/{LANGUAGE}")

for file in files :
  if file == ".ipynb_checkpoints" and (file in cleanedFiles) :
    continue
  with open(f"./data/raw/subtitles/{LANGUAGE}/{file}", 'r') as subFile :
    with open(f"./data/clean/subtitles/{LANGUAGE}/{file}", 'w') as cleanFile :
      cleanFile.write(clean_subtitle(subFile.read()))

with open(f"./data/raw/labels.txt", 'r') as labelFile :
  with open(f"./data/clean/labels.txt", 'w') as cleanLabelFile :
    cleanLabelFile.write(labelFile.read())

with open(f"./data/raw/sub_downloaded.txt", 'r') as subFile :
  with open(f"./data/clean/sub_downloaded.txt", 'w') as cleansubFile :
    cleansubFile.write(subFile.read())

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Done ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`")

print()


sentenceData = [] # [[imdb_id, [sentences], label], ... ]
wordData = [] # [[imdb_id, [words], label], ... ]

# import labels :
labelDict = dict()
if os.path.exists("./data/clean/labels.txt") :
  with open("./data/clean/labels.txt", 'r') as labelFile :
    for line in labelFile :
      line = line.split()
      labelDict[line[0]] = line[1]


print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Making DataFrame ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

files = os.listdir(f"./data/clean/subtitles/{LANGUAGE}")

for file in files :
  if file == ".ipynb_checkpoints" :
    continue
  with open(f"./data/clean/subtitles/{LANGUAGE}/{file}", 'r') as subFile :
    sentences = subFile.read().split('\n')
    sentenceData.append([file.split(".txt")[0], sentences, labelDict[file.split(".txt")[0]]])
    wordData.append([file.split(".txt")[0], sentence2word(sentences), labelDict[file.split(".txt")[0]]])

sentenceDf = pd.DataFrame(sentenceData, columns=['imdb_id', 'sentences', 'label'])
wordDf = pd.DataFrame(wordData, columns=['imdb_id', 'words', 'label'])

print()

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  create sentence and word broken csv ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

sentenceDf.to_csv('./data/sentencebroken/data.csv', index=False)
wordDf.to_csv('./data/wordbroken/data.csv', index=False)

print(sentenceDf)
print()
print(wordDf)

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Done ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")



print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Data Frame label based ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

# dataframes :
dfs = { "NC-17" : [], "PG-13" : [], "G" : [], "R" : [], "PG" : []}

for index, row in sentenceDf.iterrows():
    dfs[row['label']].append([row['imdb_id'], row['sentences']])

for label in dfs.keys() :
  labelDf = pd.DataFrame(dfs[label], columns=['imdb_id', 'sentences'])
  labelDf.to_csv(f'./data/sentencebroken/{label}.csv', index=False)
  print(labelDf)


print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Done ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")




print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ making test and train files for hugging face ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


# Split the dataframe into train and test
train_df, test_df = train_test_split(sentenceDf, test_size=0.2, random_state=42)

# Save train and test data to CSV files
train_df.to_csv('./data/sentencebroken/train.csv', index=False)
test_df.to_csv('./data/sentencebroken/test.csv', index=False)

print(train_df)
print(test_df)

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Done ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

