from asyncore import write
import random 
import os
# from  import *
import ratcliff.ratcliff
from search import *
from jaccard_search import *
import spacy
from scipy.stats import spearmanr
import csv
from matplotlib import pyplot as plt

plt.rcParams["figure.figsize"] = [50.0, 10.0]
plt.rcParams["figure.autolayout"] = True

nlp = spacy.load('en_core_web_sm')

def create_random_query():
    docs = os.listdir("./data")
    doc = docs[random.randint(1, 50)]

    # print("Document Selected: " + doc)
    # print()

    query_length = random.randint(1, 10)

    # print("Query Length: " + str(query_length))
    # print()

    with open("./data/" + doc, encoding = 'utf-8') as f:
        words = f.read()

    words = words.split(' ')

    query_start_idx = random.randint(1, int(len(words) / 2))
    # print("Query Start Index: " + str(query_start_idx))
    # print()

    query_list = words[query_start_idx:query_start_idx + query_length]
    # print("Query: " + query)
    # print()
    query = ""
    for i in query_list:
        query += i + " "

    scores = get_scores(20, query)
    # print(scores)
    # print()

    return scores, query

def get_srcc_scores():
    tfidf_tuples, query = create_random_query()
    # print(tfidf_tuples)
    tfidf_scores = []
    for score in tfidf_tuples:
        tfidf_scores.append(score[1])

    doc2vec_scores = list()
    jaccard_scores = list()
    ratcliff_scores = list()

    # print()
    # print("Scores: ")
    # print(tfidf_scores)
    # print()
    # print("Query: " + query)
    # print()

    tokenized_query = nlp(query)
    doc2vec_scores = list()
    for score in tfidf_tuples:
        doc = score[0]
        with open("./data/" + doc, encoding = 'utf-8') as f:
            doc_words = f.read()
        temp_doc = nlp(doc_words)
        doc2vec_scores.append(temp_doc.similarity(tokenized_query))
        ratcliff_scores.append(ratcliff(doc_words, query))

        jaccard_score = get_jaccardian_similarity(doc_words.split(' '), query.split(' '))
        jaccard_scores.append(jaccard_score)

    # print()
    # print("Doc2Vec Scores: ")
    # print(doc2vec_scores)
    # print()

    pvalue_tfidf, srcc_tfidf = spearmanr(tfidf_scores, doc2vec_scores)
    pvalue_jaccard, srcc_jaccard = spearmanr(jaccard_scores, doc2vec_scores)
    pvalue_ratcliff, srcc_ratcliff = spearmanr(ratcliff_scores, doc2vec_scores)

    # print("Spearman Rank Correlation Coefficient for TFIDF: " + str(srcc_tfidf) + " with query length: " + str(len(query)))

    # print("Spearman Rank Correlation Coefficient for Jaccard: " + str(srcc_jaccard) + " with query length: " + str(len(query)))

    # print("Spearman Rank Correlation Coefficient for Ratcliff-Oberschelp: " + str(srcc_ratcliff) + " with query length: " + str(len(query)))

    # print()

    return [len(query), srcc_tfidf, srcc_jaccard, srcc_ratcliff]

def get_sample_scores(num_scores):
    f = open('data.csv', 'a')
    header = ["query_length", "tfidf_srcc", "jaccard_srcc", "ratcliff_srcc"]
    writer = csv.writer(f)
    writer.writerow(header)
    for i in range(num_scores):
        print(i)
        data = get_srcc_scores()
        writer.writerow(data)
    # print()

def plot_scores():
    with open('data.csv', 'r') as f:
        reader = csv.reader(f)
        tfidf_x = []
        jaccard_x = []
        ratcliff_x = []
        tfidf_y = []
        jaccard_y = []
        ratcliff_y = []
        for row in reader:
            if row[0] == "query_length":
                continue
            tfidf_x.append(row[0])
            tfidf_y.append(row[1])
            jaccard_x.append(row[0])
            jaccard_y.append(row[2])
            ratcliff_x.append(row[0])
            ratcliff_y.append(row[3])
        tfidf_x = np.array(tfidf_x)
        tfidf_y = np.array(tfidf_y)
        jaccard_x = np.array(jaccard_x)
        jaccard_y = np.array(jaccard_y)
        ratcliff_x = np.array(ratcliff_x)
        ratcliff_y = np.array(ratcliff_y)
        plt.scatter(tfidf_x, tfidf_y, color = 'blue')
        plt.scatter(jaccard_x, jaccard_y, color = 'green')
        plt.scatter(ratcliff_x, ratcliff_y, color = 'red')
    plt.show()
                
def main():
    plot_scores()

if __name__ == '__main__':
    main()
