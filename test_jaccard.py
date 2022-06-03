# import pytest
from gettext import find
from jaccard_search import create_bag_of_words, find_intersection, find_union, get_jaccardian_similarity

def test_create_bag_of_words():
    dictionary = create_bag_of_words(set(["Apple", "Banana", "Mango", "Mango", "Mango", "Banana"]), ["Apple", "Banana", "Mango", "Mango", "Mango", "Banana"])
    assert dictionary["Apple"] == 1
    assert dictionary["Banana"] ==2

def test_find_union():
    document = create_bag_of_words(set(["Apple", "Banana", "Mango", "Mango", "Mango", "Banana"]), ["Apple", "Banana", "Mango", "Mango", "Mango", "Banana"])
    query = create_bag_of_words(set(["Apple", "Apple", "Banana"]), ["Apple", "Apple", "Banana"])
    assert find_union(query, document) == 7
    assert find_union(document, query) == 7

def test_find_intersection():
    document = create_bag_of_words(set(["Apple", "Banana", "Mango", "Mango", "Mango", "Banana"]), ["Apple", "Banana", "Mango", "Mango", "Mango", "Banana"])
    query = create_bag_of_words(set(["Apple", "Apple", "Banana"]), ["Apple", "Apple", "Banana"])
    assert find_intersection(query, document) == 2
    assert find_intersection(document, query) == 2

def test_driver():
    document = ["Apple", "Banana", "Mango", "Mango", "Mango", "Banana"]
    query = ["Apple", "Apple", "Banana"]
    assert get_jaccardian_similarity(document, query) == 3.5
    assert get_jaccardian_similarity(query, document) == 3.5

def test_driver_no_overlap():
    document = ["Mesopotamia", "is", "the", "greatest", "of", "the", "ancient", "civilizations", "on", "this", "planet"]
    query = ["pigs", "are", "smart"]
    assert get_jaccardian_similarity(document, query) == float("inf")