# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 21:01:15 2020

@author: Michael Perry
"""
import pandas as pd
import numpy as np
import os
import glob
from rake_nltk import Rake
from fuzzywuzzy import process, fuzz
import matplotlib.pyplot as plt

#Delete Combined_CSV if it exists
if os.path.exists("combined_csv.csv"):
    os.remove("combined_csv.csv")
#Read all CSV files in working directory
extension = 'csv'
af = [i for i in glob.glob('*.{}'.format(extension))]
combined_csv = pd.concat([pd.read_csv(f) for f in af ], sort = True)
combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')

#Read files
Steam = pd.read_csv('steam.csv', sep = ',')
#SteamDesc = pd.read_csv('steam_description_data.csv', sep = ',')
Netf = pd.read_csv('movies.csv', sep = ',')

#confirm columns visually
#print(Steam.columns)
#print(Netf.columns)
#SGenre = Steam['steamspy_tags'].tolist()
#SGenre.append (Steam['name'].tolist())
#NGenre = Netf['genres'].tolist()
#NGenre.append (Netf['title'].tolist())
#print(NGenre)
#uniqueSG = []
#uniqueNG = []
#testSG = []
#testNG = []
#Flatten SGenre ---------------------------------------------------------------

#for x in SGenre:
#    if ';' in x:
#        SGenre.append(x.split(';'))
#for x in SGenre:
#    if ',' in x:
#        SGenre.append(x.split(','))
#for x in SGenre:
#    if ' ' in x:
#        SGenre.append(x.split(' '))
#for x in SGenre:
#    if '-' in x:
#        SGenre.append(x.split('-'))
#for x in SGenre:
#    if type(x) == list:
#        i=0
#        while i<len(x):
#            SGenre.append(x[i])
#            i+=1
#for x in SGenre:
#    if x not in uniqueSG and type(x) != list and ';' not in x and ' ' not in x and ',' not in x and '-' not in x:
#        uniqueSG.append(x)
#print('uniqueSG---------------------------------------------------------------------')
##uniqueSG = [word for word in uniqueSG if any(letter in allowed for letter in word)]
#uniqueSG = [x.lower() for x in uniqueSG]
#print(uniqueSG)
##Flatten NGenre----------------------------------------------------------------
#or x in NGenre:
#    if ',' in x:
#        NGenre.append(x.split(','))
#for x in NGenre:
#    if ' ' in x:
#        NGenre.append(x.split(' '))
#for x in NGenre:
#    if ' ' in x:
#        NGenre.append(x.split('|'))
#for x in NGenre:
#    if ' ' in x:
#        NGenre.append(x.split('('))
#for x in NGenre:
#    if ' ' in x:
#        NGenre.append(x.split(')'))
#for x in NGenre:
#    if '-' in x:
#        NGenre.append(x.split('-'))
#for x in NGenre:
#    if type(x) == list:
#        i=0
#        while i<len(x):
#            NGenre.append(x[i])
#            i+=1
#for x in NGenre:
#    if x not in uniqueNG and type(x) != list and ',' not in x and ' ' not in x and '|' not in x and ')' not in x and '(' not in x and '-' not in x:
#        uniqueNG.append(x)
#
#for x in NGenre:
#    if type(x) != list and ',' not in x and ' ' not in x and '|' not in x and ')' not in x and '(' not in x and '-' not in x:
#        testNG.append(x)
##testNG = [word for word in testNG if any(letter in allowed for letter in word)]
## Clean up NGenre -------------------------------------------------------------
##testNG = [x.lower() for x in testNG]
#for k in testNG:
#        if "genres" in k:
#            testNG.remove(k)
#testNG = list(filter(None, testNG))
#testNG = list(filter(lambda x: x not in 'genres', testNG))
#testNG = list(filter(lambda x: x not in 'IMAX', testNG))
#testNG = list(filter(lambda x: x not in 'Fi', testNG))
#uniqueNG = list(filter(None, uniqueNG))
#uniqueNG = list(filter(lambda x: x not in 'genres', uniqueNG))
#uniqueNG = list(filter(lambda x: x not in 'IMAX', uniqueNG))
#uniqueNG = list(filter(lambda x: x not in 'Fi', uniqueNG))
##uniqueNG = [word for word in uniqueNG if any(letter in allowed for letter in word)]
##uniqueNG = [x.lower() for x in uniqueNG]
#print('uniqueNG---------------------------------------------------------------------')
#print(uniqueNG)
##print (SGenre)
##print (NGenre)
##for i in uniqueSG:
##    Netf['weight'] = Netf.apply(lambda row: 1 if i in Netf('description') else 0, axis=1)
##print(Netf['weight'])
##Compare SGenre to NGenre------------------------------------------------------
##Vocabulary -------------------------------------------------------------------
#stop_words = np.array([
#"a", "about", "above", "across", "after", "afterwards", 
#"again", "all", "almost", "alone", "along", "already", "also",    
#"although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and",
# "another", "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are", "as",
# "at", "be", "became", "because", "become","becomes", "becoming", "been", "before", "behind",
# "being", "beside", "besides", "between", "beyond", "both", "but", "by","can", "cannot", "cant",
# "could", "couldnt", "de", "describe", "do", "done", "each", "eg", "either", "else", "enough", "etc",
# "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "find","for",
# "found", "four", "from", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he",
# "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him",
# "himself", "his", "how", "however", "i", "ie", "if", "in", "indeed", "is", "it", "its", "itself",
# "keep", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mine", "more",
# "moreover", "most", "mostly", "much", "must", "my", "myself", "name", "namely", "neither", "never",
# "nevertheless", "next","no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere"
# , "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise",
# "our", "ours", "ourselves", "out", "over", "own", "part","perhaps", "please", "put", "rather", "re",
# "same", "see", "seem", "seemed", "seeming", "seems", "she", "should","since", "sincere","so",
# "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such",
# "take","than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter",
# "thereby", "therefore", "therein", "thereupon", "these", "they",
#"this", "those", "though", "through", "throughout",
#"thru", "thus", "to", "together", "too", "toward", "towards",
#"under", "until", "up", "upon", "us",
#"very", "was", "we", "well", "were", "what", "whatever", "when",
#"whence", "whenever", "where", "whereafter", "whereas", "whereby",
#"wherein", "whereupon", "wherever", "whether", "which", "while", 
#"who", "whoever", "whom", "whose", "why", "will", "with",
#"within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves"
#,'II', 'City', '&', ', ', 'Only', 'Mini', 'Your', 'Great', 'Cold', 'Female', 'Twin', 'Awkward',
#'Grand', 'Snow', 'Short', 'Epic', 'I', '', 'fi', 'Fi'
#])
#    
#for i in stop_words:
#    for k in uniqueSG:
#        if i == k:
#            uniqueSG.remove(i)
##------------------------------------------------------------------------------
#print('uniquetest-------------------------------------------------------------')
#test = []
#for i in uniqueSG:
#    for k in testNG:
#        if i == k:
#            test.append(i)
#
##Make a unique list of matched terms ------------------------------------------
#uniquetest = []
#for x in test:
#    if x not in uniquetest:
#        uniquetest.append(x)
#print(uniquetest)
#print('test-------------------------------------------------------------------')
#print(test)
#print('testNG-----------------------------------------------------------------')
#print(testNG)
#print('total matching keywords: ', len(test))
#print('total movie keywords: ', len(testNG))
#print('percent of matching keywords: ' , round(len(test)/len(testNG)*100, 2), '%')
#

#Training------------------------------------------------------------------------------
print('Begin Data Frame ------------------------------------------------------')
df = Netf

df = df[['title','genres']]
df.head()
df['Key_words'] = ""


print('Clean Genres ----------------------------------------------------------')
for index, row in df.iterrows():
    plot = row['genres']
    r= Rake()
    
    r.extract_keywords_from_text(plot)
    
    key_words_dict_scores = r.get_word_degrees()
    
    row['Key_words'] = list(key_words_dict_scores.keys())
df.drop(columns = ['genres'], inplace = True)
print('Create bag of words for movies-----------------------------------------')
df['bag_of_words'] =''

columns = df.columns
for index, row in df.iterrows():
    words = ''
    for col in columns:
        if col == 'Key_words':
            words = words+ ' '.join(row[col])+' '
    row['bag_of_words'] = words
df.drop(columns = ['Key_words'], inplace = True)
print(df,'\n')
print('Import Steam Games Data and clean it ----------------------------------')
Steam = Steam[['name','steamspy_tags']]
Steam.head()
Steam['Key_words'] = ""


print('Clean SteamSpy_Tags ---------------------------------------------------')
for index, row in Steam.iterrows():
    plot = row['steamspy_tags']
    r= Rake()
    
    r.extract_keywords_from_text(plot)
    
    key_words_dict_scores = r.get_word_degrees()
    
    row['Key_words'] = list(key_words_dict_scores.keys())
Steam.drop(columns = ['steamspy_tags'], inplace = True)

print('Create bag of words for steam -----------------------------------------')
Steam['bag_of_words'] =''

columns = Steam.columns
for index, row in Steam.iterrows():
    words = ''
    for col in columns:
        if col == 'Key_words':
            words = words+ ' '.join(row[col])+' '
    row['bag_of_words'] = words
Steam.drop(columns = ['Key_words'], inplace = True)
print(Steam,'\n')

print('Import User Games ------------------------------------------------------')
USteam = pd.read_csv('SteamUserDATA.csv', sep = ',')
UGames = USteam['Games'].tolist()
print(UGames,'\n')

print('Grab user game data from steam -----------------------------------------')
USG = Steam[(Steam['name'].isin(UGames))]
print(USG,'\n')
Check = USG['bag_of_words'].tolist()
print('Recommendations --------------------------------------------------------')
similarity = []

for i in df.bag_of_words:
    ratio = process.extract(i, USG.bag_of_words, limit=1)
    similarity.append(ratio[0][1])
df['similarity'] = pd.Series(similarity)
df.head(3)
df = df.sort_values(by=['similarity'], ascending=False)
df.drop(columns = ['bag_of_words'], inplace = True)
df = df.iloc[:25]
print(df)    
df.to_csv('result.csv', header=True, index=False)

print('Make data plot ---------------------------------------------------------')
df.plot(x = 'Movie Title', y = 'Similarity', kind = 'barh')
#plt.show()
plt.savefig('chart.png' , bbox_inches = 'tight')