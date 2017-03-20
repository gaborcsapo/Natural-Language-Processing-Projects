# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 11:19:15 2017

@author: Gabor
"""
import string
import math
import operator
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer

stop_words = ['a','the','an','and','or','but','about','above','after','along','amid','among',\
                           'as','at','by','for','from','in','into','like','minus','near','of','off','on',\
                           'onto','out','over','past','per','plus','since','till','to','under','until','up',\
                           'via','vs','with','that','can','cannot','could','may','might','must',\
                           'need','ought','shall','should','will','would','have','had','has','having','be',\
                           'is','am','are','was','were','being','been','get','gets','got','gotten',\
                           'getting','seem','seeming','seems','seemed',\
                           'enough', 'both', 'all', 'your' 'those', 'this', 'these', \
                           'their', 'the', 'that', 'some', 'our', 'no', 'neither', 'my',\
                           'its', 'his' 'her', 'every', 'either', 'each', 'any', 'another',\
                           'an', 'a', 'just', 'mere', 'such', 'merely' 'right', 'no', 'not',\
                           'only', 'sheer', 'even', 'especially', 'namely', 'as', 'more',\
                           'most', 'less' 'least', 'so', 'enough', 'too', 'pretty', 'quite',\
                           'rather', 'somewhat', 'sufficiently' 'same', 'different', 'such',\
                           'when', 'why', 'where', 'how', 'what', 'who', 'whom', 'which',\
                           'whether', 'why', 'whose', 'if', 'anybody', 'anyone', 'anyplace', \
                           'anything', 'anytime' 'anywhere', 'everybody', 'everyday',\
                           'everyone', 'everyplace', 'everything' 'everywhere', 'whatever',\
                           'whenever', 'whereever', 'whichever', 'whoever', 'whomever' 'he',\
                           'him', 'his', 'her', 'she', 'it', 'they', 'them', 'its', 'their','theirs',\
                           'you','your','yours','me','my','mine','I','we','us','much','and/or'
                           ] + list(string.punctuation) + ['1','2','3','4','5','6','7','8','9']

#I am using the snowball stemmer
stemmer = SnowballStemmer("english")

#calculates the frequency of each word on the line passed and puts it in the dictionary
def calc_tf(line, dic):
    line = line.translate(line.maketrans("","", string.punctuation))
    line = word_tokenize(line.strip().lower())
    for word in line:
        stemmed = stemmer.stem(word)
        if stemmed not in stop_words:
            if stemmed not in dic:
                dic[stemmed] = 1
            else:
                dic[stemmed] += 1

#calcualtes the idf for the words that are passed in as dimensions
def calc_idf(dic, dimensions):
    no_of_docs = 0
    for ID in dic:
        no_of_docs += 1
    
    idf = {}
    for dim in dimensions:
        idf[dim] = 0
        for ID in dic:
            if dim in dic[ID]:
                idf[dim] += 1
    for dim in idf:
        if idf[dim] != 0:
            idf[dim] = 1+math.log(no_of_docs/idf[dim])
        else:
            idf[dim] = 1
    
    return idf

#calculates tfidf based on the idf and tf and the dimensions passed in
def calc_tfidf(tf, idf, dimensions):
    tfidf = {}
    for ID in tf:
        tfidf[ID] = {}
        for dim in dimensions:
            if dim in tf[ID]:
                tfidf[ID][dim] = tf[ID][dim] * idf[dim]
            else:
                tfidf[ID][dim] = 0       
    return tfidf

#helper function to calculate dot product
def dot_product(K, L):
    if len(K) != len(L):
      return 0
    return sum(i[0] * i[1] for i in zip(K, L))

#calcualtes cosine similarity of v1 and v2
def cosine_similarity(v1, v2):
    prod = dot_product(v1, v2)
    len1 = math.sqrt(dot_product(v1, v1))
    len2 = math.sqrt(dot_product(v2, v2))
    if (len1 * len2) == 0:
        return 0.1
    return prod / (len1 * len2)

#return the cosine similarity of the query and the abstracts passed in based on the dims parameter
def compare_vectors(query, abstract, dims):
    v1 = []
    v2 = []
    for i in dims:
        v1.append(query[i])
        v2.append(abstract[i])
    return cosine_similarity(v1, v2)   

queries = {}
abstracts = {}
ID = ''
i = 0
#opens queries and read the lines. using the tf function, it calculates the term frequency
with open("cran.qry", "r") as queryfile:
    for line in queryfile:
        if line[0:2] == '.I':
            i += 1
            ID = i
        elif line.strip() == '.W':
            queries[ID] = {}
        else:
            calc_tf(line, queries[ID])
#same as above but for the abstracts
with open("cran.all.1400", "r") as queryfile:
    for line in queryfile:
        if line[0:2] == '.I':
            ID = line[3:].strip()
        elif line[0:2] == '.A':
            ignore = True
        elif line[0:2] == '.B':
            ignore = True
        elif line[0:2] == '.T':
            ignore = True
        elif line.strip() == '.W':
            ignore = False
            abstracts[ID] = {}
        elif not ignore:
            calc_tf(line, abstracts[ID])

result = {}
i = 0
#for each query it calculates the idf and tfidf ffor the query and all other abstracts, then calcualtes the cos sim
for ID in queries:
    dimensions = list(queries[ID].keys())
    #dimensions = [x for x in queries[ID].keys() for dim in range(queries[ID][x])]
    query_idf = calc_idf(queries, dimensions)
    query_tfidf = calc_tfidf({ID: queries[ID]}, query_idf, dimensions)
    abstract_idf = calc_idf(abstracts, dimensions)
    abstract_tfidf = calc_tfidf(abstracts, abstract_idf, dimensions)
    result[ID] = {}
    for ID2 in abstract_tfidf:
        result[ID][ID2] = compare_vectors(query_tfidf[ID], abstract_tfidf[ID2], dimensions)
        
#formatting and writing output into file
output = open('results.txt', 'w')
query_id = list(result.keys()) 
query_id.sort()   
for ID in query_id:  
    sorted_ = sorted(result[ID].items(), key=operator.itemgetter(1))
    for i in range(len(sorted_)):
        output.write(str(ID) + ' ' + str(sorted_[len(sorted_)-i-1][0]) + ' ' + str(sorted_[len(sorted_)-i-1][1]) + '\n')
    
