import jieba
import jieba.posseg as pseg
import jieba.analyse as ans

import csv

import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

jieba.suggest_freq('5月', True)
jieba.suggest_freq('老男人', True)
jieba.suggest_freq('什么鬼', True)
jieba.suggest_freq('文化自信', True)
jieba.suggest_freq('跌了', True)
jieba.suggest_freq('特朗普', True)
jieba.suggest_freq('川普', True)


##extract content column from spreadsheet
content_list = []
path = 'TrTwAllCompleteMay07080910th.csv'
with open(path) as content:
   reader=csv.reader(content,delimiter=',')
   for row in reader:
       content_list.append(row[3])
##remove title of the column
content_list.remove('content')


##tokenization (jieba)
for i in range(len(content_list)):
    document_cut = jieba.cut(content_list[i])
    result = '/'.join(document_cut)
    content_list[i]=result


##import stopword txt
sw_path = "stop_words.txt"
sw_dic = open(sw_path, 'rb')
sw_content = sw_dic.read().decode('utf-8')
##sw_content = sw_dic.read()
#convert txt to stopwords list
sw_list = sw_content.splitlines()
sw_dic.close()


##vectorize
corpus = content_list
cntVector = CountVectorizer(stop_words=sw_list)
##term frequency-inverse document frequency
cntTf = cntVector.fit_transform(corpus)


##to access words bag: wordlist = vector.get_feature_names()
##tfidf_feature_names = tfidf_vectorizer.get_feature_names()

tf_vectorizer = CountVectorizer(stop_words=sw_list)
tf = tf_vectorizer.fit_transform(corpus)
tf_feature_names = tf_vectorizer.get_feature_names()


lda = LatentDirichletAllocation(n_components=20,doc_topic_prior=0.001,topic_word_prior=0.8,learning_offset=50.,random_state=0).fit(tf)
docres = lda.fit_transform(cntTf)

def display_topics(model, feature_names, no_top_words):

    for topic_idx, topic in enumerate(model.components_):

        print("Topic %d:" % (topic_idx))
        print(" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))


no_top_words = 20

#print(docres)
display_topics(lda, tf_feature_names, no_top_words)

