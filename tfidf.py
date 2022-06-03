import numpy as np
import pandas as pd
# import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os, pickle

def create_set_of_words(files: list) -> set[str]:
    """
        Parameters: set_of_words: set[str]
            - No parameters required. Accesses the files from the directory of the repository
        Returns: dict[str, int]
            - Set containing all words present in all documents relevant to the query without stopwords
        Functionality:
            - Create a set of words present in all documents for furthur use without the stopwords
    """
    set_of_words = set({})
    for file in files:
        with open("./data/" + file, encoding = 'utf-8') as f:
            file_words = f.read()
            tokenized_file_words = word_tokenize(file_words)
            for word in tokenized_file_words:
                if word not in set(stopwords.words('english')):
                    set_of_words.add(word)
    return set_of_words

def create_bag_of_words(set_of_words: set[str], words: list) -> dict[str, int]:
    """
        Parameters: set_of_words: set[str]
            - Takes in a set of words containing all the words in all the documents and a list of words in all the documents
        Returns: dict[str, int]
            - Dict with keys as the word and value as the number of occurences of the word in the document
        Functionality:
            - Calculates the number of occurences of words in a set of words
    """
    bow = dict.fromkeys(set_of_words, 0)
    for word in words:
        bow[word] = words.count(word)
    return bow

def calculate_term_freq(bag_of_words: dict[str, int]) -> dict[str, int]:
    """
        Parameters: bag_of_words: dict[str, int]
            - Takes in a dict in the form of a bag of words, with keys as the words in all the documents and 
              value as the number of occurences of the word in all the documents
        Returns: tf: dict[str, int]
            - Dict with the keys as the word and value as the term frequency of the word in all the documents
        Functionality: 
            - Calculates the term frequency of words in all the documents
    """
    tf = {}
    bow_count = len(bag_of_words)
    for word, counter in bag_of_words.items():
        tf[word] = counter / float(bow_count)
    return tf

def calculate_inverse_doc_freq(bags_of_words: list) -> dict[str, int]:
    """
        Parameters: bags_of_words : list(dict[str, int])
            - Takes in a list of bag of words corresponding to each document
        Returns: idf_dict : dict[str, int]
            - Dict with keys as teh word and value as the inverse document frequency of the word in all the documents
        Functionality:
            - Calculates the inverse document frequnecy of words in all the documents
    """
    num_documents = len(bags_of_words)
    idf_dict = dict.fromkeys(bags_of_words[0].keys(), 0)
    for bag_of_words in bags_of_words:
        for word, value in bag_of_words.items():
            if value > 0:
                idf_dict[word] += 1
    for word, value in idf_dict.items():
        idf_dict[word] = np.log(num_documents / (float(value) + 1))
    return idf_dict

def helper_calculate_tf_idf(tf_bow: dict[str, int], idfs: list) -> dict[str, int]:
    """
        Parameters: tf_bow: dict[str, int], idfs: list
            - Takes in a dict in the form of a bag of words with keys as the word in a document with value as the term
            frequency of the word in the document and a list containing the inverse document frequencies of words in
            the document
        Returns: dict[str, int]
            - Returns a dict[str, int] with keys as the words in a document and value as the term frequency inverse
            document frequency of the words in a document
        Functionality:
            - Calculates the term frequency inverse document frequency of words in all the documents
    """
    tf_idf = {}
    for word, value in tf_bow.items():
        tf_idf[word] = value * idfs[word]
    return tf_idf

def calculate_tf_idf(files: list, set_of_words: set[str], idfs: list) -> list:
    """
        Parameters: set_of_words: set[str], idfs: list
            - Takes in a set of words containing all the words in all the documents and a list which contains the
              inverse document frequencies of all words in every documents
        Returns: list
            - Returns a list of term-frequency-inverse-document-frequency corresponding to each document
        Functionality:
            - Calculates the tfidf scores of each document 
    """
    tfidfs = []
    for file in files:
        with open("./data/" + file, encoding = 'utf-8') as f:
            file_words = f.read()
            tokenized_file_words = word_tokenize(file_words)
            tokenized_file_words = [word for word in tokenized_file_words if word not in set(stopwords.words('english'))]
            bag_of_words = create_bag_of_words(set_of_words, tokenized_file_words)
            tf = calculate_term_freq(bag_of_words)
            tfidf = helper_calculate_tf_idf(tf, idfs)
            tfidfs.append(tfidf)
    return tfidfs

def documents_bag_of_words(files: list, set_of_words: set[str]) -> list[str]:
    """
        Parameters: set_of_words: set[str]
            - Takes in a set of words containing all the words in all the documents
        Returns: list
            - Returns a list of the tfidf scores of every document present in the directory
        Functionality:
            - Calculates the bag of words index for every document present in the directory and returns a list of them
    """
    bags_of_words = []
    for file in files:
        with open("./data/" + file, encoding = 'utf-8') as f:
            file_words = f.read()
            tokenized_file_words = word_tokenize(file_words)
            tokenized_file_words = [word for word in tokenized_file_words if word not in set(stopwords.words('english'))]
            bag_of_words = create_bag_of_words(set_of_words, tokenized_file_words)
            bags_of_words.append(bag_of_words)
    return bags_of_words

def create_dataframe(files) -> pd.DataFrame:
    """
        Parameters: 
            - No parameters required
        Returns: list
            - Returns a list of the bag_of_words score of every document present in the directory
        Functionality:
            - Calculates the tfidf score index for every document present in the directory and returns a list of them
    """
    set_of_words = create_set_of_words(files) 
    bags_of_words = documents_bag_of_words(files, set_of_words)
    idfs = calculate_inverse_doc_freq(bags_of_words)
    tfidfs = calculate_tf_idf(files, set_of_words, idfs)

    df_tfidfs = pd.DataFrame(tfidfs)

    with open("inverted_index.pkl", "wb") as f:
        pickle.dump(df_tfidfs,f, protocol = pickle.HIGHEST_PROTOCOL)
    return df_tfidfs

def main() -> None:
    files = os.listdir("./data")
    dataframe = create_dataframe(files)
    print(dataframe)

if __name__ == "__main__":
    main()
