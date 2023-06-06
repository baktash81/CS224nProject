import requests
from bs4 import BeautifulSoup
import json
import pickle
import time
from imdb import Cinemagoer, IMDbError
from collections import defaultdict
import os
import random

def get_imdb_ids(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    movie_links = soup.select('.lister-item-header a[href^="/title/"]')
    imdb_ids = [link['href'].split('/')[2] for link in movie_links]
    return imdb_ids


def downSub(lang,imdbId,apiToken) :

  dir = "./data/raw/subtitles/eng/"
  try :
    headers = {
      'Api-Key': apiToken,
      'Content-Type': 'application/json'
    }
    response = requests.post(f'https://api.opensubtitles.com/api/v1/subtitles?imdb_id={imdbId}&languages={lang}&order_by=ratings', headers=headers)
    if response.status_code == 200:
      response = response.json()
      if response["total_count"] > 0 :
        subid = response["data"][0]["attributes"]["files"][0]["file_id"]
        response2 = requests.post(f'https://api.opensubtitles.com/api/v1//download', headers=headers, json = {"file_id": subid})
        if response2.status_code == 200 :
          response2 = response2.json()
          url = response2["link"]
          subtitle = requests.get(url, allow_redirects=True)

          open(f'{dir}{imdbId}.txt', 'w').write(subtitle.text)

          return True



    return False

  except Exception as e:
    print(e)
    return False



print("$$$$$$$$$$$$$$$$$$$$$$$$ Start crawling imdb ids $$$$$$$$$$$$$$$$$$$$$$$$")

num_pages = int(input("Enter number of page (each page  = 50 imdb ids : )"))
base_url = 'https://www.imdb.com/search/title/?title_type=feature&start='

all_imdb_ids = []
for page in range(1, num_pages + 1):
    start_index = (page - 1) * 50
    url = base_url + str(start_index)
    imdb_ids = get_imdb_ids(url)
    all_imdb_ids.extend(imdb_ids)

print("number of ids :",len(all_imdb_ids))
print()
print("$$$$$$$$$$$$$$$$$$$$$$$$ Done $$$$$$$$$$$$$$$$$$$$$$$$")


print()
print("$$$$$$$$$$$$$$$$$$$$$$$$ Start crawling labels and downloading subtitles $$$$$$$$$$$$$$$$$$$$$$$$")
print()
print("Note that you can use your Open Subtitle account tokens but now we use my tokens")
print()

## your open subtitle account token
TOKENS = ['LDkM48z0z3vqC7cBt3P2P3v1bYqfp3hT', '7kVKJYjyBQZFvvE4lUnbKYl780N2oaEA',
          'MlHoSwyh94tp35Ekp8Uv1ky8HXIWDjLS', 'MI0ke5UYBsa46sZ3qktUsU2IJ05dLWnY',
          'kWfSPpPdQmR0HYaTZRWCGWGsDNMn5QM2', 'lvGFXoqn9CPwOgwsuCCULRPwmd5z31VF']

SUB_LANGUAGE = 'en'

# number of subtitle to download

NUMS = int(input("Enter number of subtitles to download (maximum 600) : "))

# declare dict for labels :
Dictlabel = defaultdict(list)
# Already donwloaded subtitles :
downloadedSubs = []

# make project data repository : 
if not os.path.exists("./data"):
    print("make Directories")
    os.makedirs("./data")
if not os.path.exists("./data/clean"):
    print("make Directories")
    os.makedirs("./data/clean")
    if not os.path.exists("./data/clean/subtitles"):
       os.makedirs("./data/clean/subtitles")
       if not os.path.exists("./data/clean/subtitles/eng"):
        os.makedirs("./data/clean/subtitles/eng")
    
if not os.path.exists("./data/raw"):
    print("make Directories")
    os.makedirs("./data/raw")
    if not os.path.exists("./data/raw/subtitles"):
       os.makedirs("./data/raw/subtitles")
       if not os.path.exists("./data/raw/subtitles/eng"):
        os.makedirs("./data/raw/subtitles/eng")
if not os.path.exists("./data/sentencebroken"):
    print("make Directories")
    os.makedirs("./data/sentencebroken")
if not os.path.exists("./data/wordbroken"):
    print("make Directories")
    os.makedirs("./data/wordbroken")

print()

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Import downloaded subtitles~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
if os.path.exists("./data/raw/sub_downloaded.txt") :
  with open("./data/raw/sub_downloaded.txt", 'r') as downloadedSub :
    lines = downloadedSub.readlines()
    for line in lines :
      downloadedSubs.append(line.split()[0])
print("Done")
print()

try :
  with open("./data/raw/labels.txt", 'a') as file2 :
    with open("./data/raw/sub_downloaded.txt", 'a') as file3 :

      ia = Cinemagoer()
      ids = all_imdb_ids
      random.shuffle(ids)
      indx = 0
      for id in ids :
        if indx == NUMS : 
          print("finished")
          break
        if id in downloadedSubs :
          continue
        movieInfo = ia.get_movie(id.replace("tt", ""))
        ## export age rate of movie :
        if 'certificates' in movieInfo : 
            for standard in movieInfo['certificates'] :
              if "United States" in standard and ("::" not in standard) and ("TV" not in standard) :
                label = standard.split("United States:")[1]
                if label in ["PG", "G", "NC-17", "R", "PG-13"] :         
                  Dictlabel[id].append(label)
                  line = f'{id} {label} \n'
                  # download subtitle
                  if downSub(SUB_LANGUAGE, id, TOKENS[indx % len(TOKENS)]) :
                    file2.write(line)
                    file3.write(id + " \n")
                    downloadedSubs.append(id)
                    indx += 1
                    print(indx, line)
                    print("Subtitle successfully downloaded :) ")
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    time.sleep(1)
                    break
                  else :
                    print("Failed :(")
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
  
except Exception as e :
  print(e)

print()
print("Done")
