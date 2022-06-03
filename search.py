import numpy as np
import pandas as pd
from tfidf import *

def cosine_similarity(x: list, y: list):
    """
        Parameters: x: numpy list, y: numpy list
            - Takes in two numpy lists that contains the tfidf score of words present in the query and a document
        Returns: float
            - Returns a score based on the cosine similarity of the query and the document
        Functionality:
            - Calculates cosine similarity between two numpy arrays of the tfidf score of document and query
    """
    x_sqrt = np.sqrt(np.dot(x, x))
    y_sqrt = np.sqrt(np.dot(y, y))
    if y_sqrt != 0:
        return (np.dot(x, y.T) / (x_sqrt * y_sqrt))
    else:
        return 0

def document_tfidf(files, dataframe: pd.DataFrame, query: list[str], total_docs: int):
    """
        Parameters: dataframe: pd.DataFrame, query: list[str], total_docs: int
            - Takes in a pandas dataframe that contains the tfidf scores corresponding to each word present in 
            all the documents,  a list of string which contains words present in the tokenized query, and the
            total number of documents that are being searched
        Returns: tuple(pd.DataFrame, list[int, float]) 
            - Returns a new datafram containing a new dataframe that has been updated based on the cosine similairty 
            algorithm based score on the words present in a query. It also returns a list that contains a list of 
            similarity scores between every document present in the set of documents and the query.
        Functionality:
            - Uses the cosine similarity algorithm and returns a list that maps the cosine similarity of the 
            query with the document index.
    """
    width = dataframe.shape[1] # width of the dataframe
    final = list() # list to store document similarity and document name

    new_df = dataframe # dataframe used for calculating cosine similarity
    document_term_value = dataframe[dataframe > 0].count().values # occurence of term in document 
    document_frequency = np.log(width / (document_term_value + 1)) # document freq of term in document

    counter = 0 # used for document index
    for doc in files: # loop through files
        result = np.zeros(width) # store tfidf values of word in document
        row =  dataframe.iloc[counter] # get row number of document (contains the words present in the document)
        row_values = row.values # values present in the row (tfidf scores of words present in the document)

        for j, term in enumerate(row.index): # Iterate through the words present in a document 
            if row_values[j] > 0: # Insert tfidf score of the word into the new dataframe
                term_frequency = np.log(row_values[j] + 1) # idf score of the word
                new_df.iloc[counter, j] = term_frequency * document_frequency[j] # tfidf score of the word
            
            elif row_values[j] == 0: # Word not present in the document (score is 0)
                term_frequency = 0
                new_df.iloc[counter, j] = 0 
            
            if term in query: # found a common word in the query and the words present in the document 
                new_column = dataframe[[term]]
                new_column_value = new_column[new_column > 0].count().values
                result[j] = term_frequency * (np.log(total_docs / (new_column_value[0] + 1))) 
        final.append((doc, cosine_similarity(new_df.loc[counter].values, result))) # Append cosine similarity score of document and query
        counter += 1
    return new_df, final # new_df for testing purposes

def tfidf_query(documents: list, query: str):
    """
        Parameters: documents: list, query : str
            - Takes in a list of documents and a query in the form of a string that is used to get the 
            similar documents based on the similarity between the query and a document
        Returns: tuple(pd.DataFrame, list[int, float])
            - Returns a tuple which contains the document index and the cosine similarity of that particular
            document with the query of all documents passed as a parameter in the list
        Functionality:
            - Returns a list containing the cosine similarity of the query with all the documents present in 
            the list passed in the parameter. Also prints the matrix containing the tfidf scores of all words
            present in all documents.
    """
    docs = os.listdir("./data")
    tokenized_query = word_tokenize(query)
    term_doc_matrix, query_tfidf = document_tfidf(docs, create_dataframe(docs), tokenized_query, len(documents))
    return query_tfidf

def get_scores(num_docs: int, query: str) -> list[int]:
    docs = os.listdir("./data")
    query_tfidf = tfidf_query(docs, query)
    scores = sorted(query_tfidf, key = lambda x : x[1], reverse = True)
    scores = scores[:num_docs]
    return scores
