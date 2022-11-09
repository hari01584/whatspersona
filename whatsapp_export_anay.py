import regex
import pandas as pd
import numpy as np
import emoji
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

def let_user_pick(options):
    print("Please choose:")

    for idx, element in enumerate(options):
        print("{}) {}".format(idx + 1, element))

    i = input("Enter number: ")
    try:
        if 0 < int(i) <= len(options):
            return int(i) - 1
    except:
        pass
    return None

def date_time(s):
    pattern = '^([0-9]+)(\/)([0-9]+)(\/)([0-9]+), ([0-9]+):([0-9]+)[ ]?(AM|PM|am|pm)? -'
    result = regex.match(pattern, s)
    if result:
        return True
    return False

def find_author(s):
    s = s.split(":")
    if len(s)==2:
        return True
    else:
        return False

def getDatapoint(line):
    splitline = line.split(' - ')
    dateTime = splitline[0]
    date, time = dateTime.split(", ")
    message = " ".join(splitline[1:])
    if find_author(message):
        splitmessage = message.split(": ")
        author = splitmessage[0]
        message = " ".join(splitmessage[1:])
    else:
        author= None
    return date, time, author, message



class WhatsappExport():
    def __init__(self, fpath):
        self.fpath = fpath

    def corpus(self):
        data = []
        conversation = self.fpath
        with open(conversation, encoding="utf-8") as fp:
            fp.readline()
            messageBuffer = []
            date, time, author = None, None, None
            while True:
                line = fp.readline()
                if not line:
                    break
                line = line.strip()
                if date_time(line):
                    if len(messageBuffer) > 0:
                        data.append([date, time, author, ' '.join(messageBuffer)])
                    messageBuffer.clear()
                    date, time, author, message = getDatapoint(line)
                    messageBuffer.append(message)
                else:
                    messageBuffer.append(line)


        self.df = pd.DataFrame(data, columns=["Date", 'Time', 'Author', 'Message'])
        self.df['Date'] = pd.to_datetime(self.df['Date'])

        total_messages = self.df.shape[0]

        media_messages = self.df[self.df["Message"]=='<Media omitted>'].shape[0]

        def split_count(text):
            emoji_list = []
            data = regex.findall(r'\X',text)
            for word in data:
                if any(char in emoji.EMOJI_DATA for char in word):
                    emoji_list.append(word)
            return emoji_list
        self.df['emoji'] = self.df["Message"].apply(split_count)

        emojis = sum(self.df['emoji'].str.len())

        URLPATTERN = r'(https?://\S+)'
        self.df['urlcount'] = self.df.Message.apply(lambda x: regex.findall(URLPATTERN, x)).str.len()
        links = np.sum(self.df.urlcount)


        print("Total Messages: ", total_messages)
        print("Number of Media Shared: ", media_messages)
        print("Number of Emojis Shared", emojis)
        print("Number of Links Shared", links)

        columns = self.df.columns.tolist()
        
        # author = list(set(i.Author for _, i in self.df.iterrows() if i.Author is not None))
        
        # res = let_user_pick(author)
        # print(author[res])
        self.corpus = []
        for _, i in self.df.iterrows():
            # print(i)
            #break
            self.corpus.append(i.Message)

        return self.corpus

    def conversational_corpus(self):
        self.corpus()

        conv = []
        author = list(set(i.Author for _, i in self.df.iterrows() if i.Author is not None))

        myauth = author
        for _, i in self.df.iterrows():
            auth = i.Author
            if(auth == myauth)
            break

if(__name__ == "__main__"):
    wexport = WhatsappExport("./whatsapp_export/WhatsApp Chat with Abhinandan Bhai Thapar.txt")
    wexport.conversational_corpus()    