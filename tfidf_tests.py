from search import *

def test_results(query: str):
    docs = os.listdir("./data")

    doc_similarity_scores = {}

    for doc in docs:
        words = ""
        with open("./data/" + doc, encoding = 'utf-8') as f:
            words += f.read()

        word_list = word_tokenize(words)
        query_list = word_tokenize(query)

        word_set = {word for word in word_list if not word in stopwords.words('english')} 
        query_set = {word for word in query_list if not word in stopwords.words('english')}

        word_vector, query_vector = [], []

        bag_of_words = word_set.union(query_set) 
        for word in bag_of_words:
            if word in word_set: 
                word_vector.append(1)
            else:
                word_vector.append(0)
            
            if word in query_set:
                query_vector.append(1)
            else:
                query_vector.append(0)
        
        similarity_score = 0
        for i in range(len(bag_of_words)):
            similarity_score += word_vector[i] * query_vector[i]

        cosine_similarity_score = similarity_score / float((sum(query_vector) * sum(word_vector)) ** 0.5)

        doc_similarity_scores[doc] = cosine_similarity_score

    return doc_similarity_scores

    # CORRECT RESULTS OBTAINED IF COSINE SIMILARITY SCORE OF TEXTS > 0 FOR TOP num_docs FILES SCORE

def validate_results(scores, num_docs: int, query: str):
    test_scores = test_results(query)
    print()
    for score in scores:
        print("Text: " + str(score[0]))
        print("Score: " + str(score[1]))
        print()
    for i in range(len(scores)):
        text = scores[i][0]
        score = scores[i][1]
        simple_score = test_scores[text]
        print("Text: " + str(text))
        print("Score using TFIDF calculator: " + str(score))
        print("Score using simple cosine similarity: " + str(simple_score))
        if score == 0:
            diff_percent = 0
        else:
            diff_percent = abs(score - simple_score) * 100 / score
        print("Difference Percentage: " + str(diff_percent) + "%")
        print()

def main(num_docs: int, query: str):
    docs = os.listdir("./data")
    query_tfidf = tfidf_query(docs, query)
    scores = sorted(query_tfidf, key = lambda x : x[1], reverse = True)
    scores = scores[:num_docs]
    validate_results(scores, num_docs, query)
    return scores

if __name__ == "__main__":
    main(7, "district")
