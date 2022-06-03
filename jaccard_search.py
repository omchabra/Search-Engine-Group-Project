def create_bag_of_words(set_of_words: "set[str]", words: list) -> "dict[str, int]":
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


def find_union(bag_first: "dict[str,int]", bag_second: "dict[str, int]") -> int:
    """
        Parameters: bag_first: dict[str,int], bag_second: dict[str,int]
            - Takes in a two dictionaries where words are mapped to their frequency in the document
        Returns: int
            - int that denotes the size of the union between the two bags of words
        Functionality:
            - Calculates the size of the union of two bags of words
    """
    keys = set.union(set(bag_first.keys()), set(bag_second.keys()))
    union = 0

    for word in keys:
        if word in bag_second.keys() and word in bag_first.keys():
            union += max(bag_first[word], bag_second[word])
        elif word in bag_first:
            union += bag_first[word]
        else:
            union += bag_second[word]
    return union


def find_intersection(bag_first: "dict[str,int]", bag_second: "dict[str, int]") -> int:
    """
        Parameters: bag_first: dict[str,int], bag_second: dict[str,int]
            - Takes in a two dictionaries where words are mapped to their frequency in the document
        Returns: int
            - int that denotes the size of the intersection between the two bags of words
        Functionality:
            - Calculates the size of the intersection of two bags of words
    """
    keys = set.intersection(set(bag_first.keys()),set(bag_second.keys()))
    intersection = 0
    for word in keys:
        intersection += min(bag_first[word], bag_second[word])
    
    return intersection


def find_jaccardian(union:int, intersection:int)->float:
    """
        Parameters: union:int, intersection:int
            - Takes in the size of the weighted union and intersection of two sets of words
        Returns: float
            - The jaccobian index for the input files
        Functionality:
            - Calculates the jaccobioan index of two sets of words
    """
    if (intersection == 0):
        return float("inf")
    return union / float (intersection)



def get_jaccardian_similarity(document: list, query:list)->float:
    """
        Parameters: document:list, query:list
            - Takes in the document and the query and generates similarity
        Returns: float
            - The jaccardian index for the input files
        Functionality:
            - Calculates the jaccardian index of two lists of words
            - Returns infinity if there is absolutely no overlap
    """
    query_bag = create_bag_of_words(set(query), query)
    doc_bag = create_bag_of_words(set(document), document)

    union = find_union(query_bag, doc_bag)
    intersection = find_intersection(query_bag, doc_bag)
    return find_jaccardian(union, intersection)
