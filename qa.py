import pandas as pd
import spacy as sp
import re

en = sp.load('en_core_web_lg')
SW = ['where', 'what', 'who', 'which']
#adding usual interogative prepositions
en.Defaults.stop_words.add('number')
en.Defaults.stop_words.add('in')
en.Defaults.stop_words.add('at')
en.Defaults.stop_words.add('to')

#removing interogative words
en.Defaults.stop_words.remove('who')
en.Defaults.stop_words.remove('what')
en.Defaults.stop_words.remove('where')
en.Defaults.stop_words.remove('which')

stop_words = en.Defaults.stop_words
signs = ['?']
dic_where = {'room':1, 'email':1, 'town':1, 'state':1, 'mailroom':1 }
dic_who = {'name':1, 'year':1, 'room':1, 'email':1, 'town':1, 'state':1, 'mailroom':1, 'email':1}
dic_what = {'year':1, 'room':1, 'email':1, 'town':1, 'state':1, 'mailroom':1, 'email':1}
dic = {'where':dic_where, 'who':dic_who, 'what':dic_what, 'which':dic_what}

def init():
    dic_year= {'F':'Freshman','T':'Freshman', 'S':'Sophomore','J':'Junior','S':'Senior'}
    dic_building = {}
    dic_building_description = {}
    df = pd.read_csv('cleantxt.txt', delimiter='\t\t', engine='python')
    li = set(df.room.values.tolist())
    for w in li:
        if w[0:2] in dic_building.keys():
            dic_building[w[0:2]] = dic_building[w[0:2]] + 1
        else:
            dic_building[w[0:2]] = 1
    

def clean(x):
    x = re.sub('\'s','',x)
    x = re.sub(r'[^\w\s]', '', x)
    return x

def compression(question):

    #remove the stopwords
    tokens = question.split()
    tokens = [clean(w) for w in tokens]
    tokens = [w for w in tokens if w not in stop_words]

    #grab the name
    question = clean(question)
    doc = en(question)
    name_ent = doc.ents[0].text
    name_ent_arr = name_ent.split()
    #print(name_ent_arr)
    for w in name_ent_arr:
        tokens.remove(w)

    #grab the interrogative question mark
    q_mark = [el for el in tokens if el.lower() in SW][0]
    tokens.remove(q_mark)

    #clean the rest
    tokens = [w.lower() for w in tokens]
    #print(tokens)
    return tokens,name_ent, q_mark    

def attention (tokens, name_ent, q_mark):
    ranking = {}

    #if empty tokens just use 1 for every column but linked to the q_m
    if len(tokens)==0:
        for key in dic[q_mark.lower()].keys():
            ranking[key] = 1

    #else if not use the dot-product to rank columns
    else:
        score = [1]*len(dic[q_mark.lower()].keys())
        i = 0
        for key in dic[q_mark.lower()].keys():
            for token in tokens:
                score[i] = score[i]*en(token).similarity(en(key))
            ranking[key] = score[i]
            i = i + 1
    return name_ent, ranking           
    
def query(name_ent, ranking, df):
    name_ent_arr = name_ent.split()
    name_ent = '"' + name_ent_arr[-1] +', ' +  name_ent_arr[0]
    pf = df[df['name'].str.contains(name_ent)]
    pf.reset_index()
    ranking = {k: v for k, v in sorted(ranking.items(), key=lambda item: item[1])}
    #print(ranking)
    L = list(ranking.keys())
    columns = [L[-1]]
    answer = 'It is ' + pf[columns[0]]
    return answer


name = input('What is your name? ')
print('Hello I am the GCC\'s wizard! For any student that you know ask me about the following:\n')
print('1)email, 2)mailroom number, 3)room number, 4)town of origin, 5)state of origin')
print('\n\n=============================================\n\n')
x = input(name + ' : ')
while x!='stop':
    df = pd.read_csv('cleantxt.txt', delimiter='\t\t', engine=
                     'python')
    df.columns = ['name', 'year', 'room', 'mailroom', 'town', 'state', 'email']
    tokens,name_ent, q_mark = compression(x)
    name_ent, ranking = attention(tokens,name_ent, q_mark)
    print(query(name_ent, ranking, df))
    print('\n\n')
    x = input(name + ' : ')
