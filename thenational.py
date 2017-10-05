#Packages Imports
import sys
import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
import re
from nltk.stem import WordNetLemmatizer
from os import path
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
from collections import Counter

USEMASK=False

path = "."
filename = "thenational.txt"

data = open(path+"\\"+filename).read()

if False:
    print(data)

    pd.options.display.max_colwidth = 200
    data.head()

    #DATA CLEANING
    all_lyrics = ""
    for index, row in data.iterrows():
        #lyrics_decoded = row['lyrics_text'].lower().decode("utf-8", "replace")
        lyrics_decoded = row['lyrics_text'].lower()
        lyrics_no_backslash = lyrics_decoded.replace("\"", "")
        all_lyrics = all_lyrics + " " + lyrics_no_backslash

    print(all_lyrics)
    #LOOKING AT THE 10 MOST COMMON WORDS
    #Tokenizing
    tok = nltk.tokenize.word_tokenize(all_lyrics)

    #Counting words
    cnt = Counter(tok)
    cnt.most_common(10)

else:
    all_lyrics = ""
    removelist = ['chorus','verse','[',']']
    for item in data.split(" "):
        item = item.lower()
        breakloop = False
        for removeitem in removelist:
            if removeitem in item:
                breakloop = True
        if not breakloop:
            all_lyrics = all_lyrics + " " + item

#print(all_lyrics)

#LOOKING AT THE 10 MOST COMMON WORDS
#Tokenizing
tok = nltk.tokenize.word_tokenize(all_lyrics)

#Counting words
cnt = Counter(tok)
cnt.most_common(20)

print(cnt.most_common(20))

if False:
    #Basic wordcloud generation test
    wc = WordCloud().generate(all_lyrics)
    plt.imshow(wc)
    plt.axis("off")
    plt.show()

tokens = nltk.tokenize.word_tokenize(all_lyrics)

wnl = WordNetLemmatizer()
lemmatized_tokens = [wnl.lemmatize(word, 'v') for word in tokens]

joined = " ".join(lemmatized_tokens)
shortword = re.compile(r'\W*\b\w{1,2}\b')
lyrics_long = shortword.sub('', joined)

lyrics_abrev = lyrics_long.replace("gon ", "go").replace("wan ", "want")

if USEMASK:
    #WORDCLOUD GENERATION SECTION
    #d = path.dirname('C:\PythonProjects\WordCloud\maskrepo')
    d = 'C:\PythonProjects\WordCloud\maskrepo'
    #Either choose a music_genre (among classical, country, dance, electro, hiphop, jazz,
    #latino, metal, reggae, reggaeton, rnb, rock, soul) and leave the artist_name variable empty ("")
    #Or if you're willing to use a specific picture, leave the music_genre parameter empty (""),
    #fill the artist_name parameter
    music_genre = ""
    artist_name = "beatles"

    if music_genre:
        mask = np.array(Image.open(path.join(d, "\\"+music_genre+".jpeg")))
    elif not music_genre:
        mask = np.array(Image.open(d+ "\\"+artist_name+".jpg"))
    else:
        print ("bug")

    wc = WordCloud(background_color="white", max_words=10000, mask=mask, random_state=42,
              font_path="C:\PythonProjects\WordCloud\word_cloud-master\wordcloud\DroidSansMono.ttf")

    wc.generate(lyrics_abrev)
    image_colors = ImageColorGenerator(mask)

    plt.imshow(wc.recolor(color_func=image_colors))
    plt.axis("off")
    plt.show()
else:

    # Generate a word cloud image
    wc = WordCloud().generate(lyrics_abrev)

    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    ## lower max_font_size
    #wc = WordCloud(max_font_size=40).generate(lyrics_abrev)
    #plt.figure()
    #plt.imshow(wc, interpolation="bilinear")
    #plt.axis("off")
    #plt.show()


