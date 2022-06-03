import json, sys, os
import requests as r

def pullWikipediaData(amt:int = 10) -> list:
    """
        Parameters: amt: int = 10
            - Takes in one argument of type int, defaulting to 10, denoting the amount of documents to scrape.
        Returns: List
            - List with each element being a dictionary containing the name and description of random wikipedia articles.
        Functionality: Returns 'amt' length list with each element being a dictionary with the description of wikipedia articles.
    """
    docs = []
    for _ in range(amt):
        response = json.loads(r.get("https://en.wikipedia.org/api/rest_v1/page/random/summary").content)
        name = response.get("title")
        print(name)
        extract = response.get("extract")

        docs.append({
            "name":name,
            "desc": extract
        })

    return docs

def writeToFile(docs: list[dict]) -> None:
    """
        Parameters: docs: list[dict]
            - Takes in one argument of type of list, with each element being a dictionary of wikipedia content.
        Returns: None
        Functionality: Creates a directory 'data' to house all of the wikipedia articles. 
            The documents will include a summary of the Wikipedia page and will be named after the wikipedia page.
            The contents of the documents are encoded in utf-8.
    """
    if not os.path.isdir("./data"):
        os.mkdir(os.path.join(os.getcwd(), 'data')) #Creates directory ./data if doesn't exist

    for i in docs:
        try:
            with open("./data/{}.txt".format(i.get("name")), 'w', encoding = 'utf8') as f: #Writes/Updates file on disk.
                f.write(i.get("desc"))
            f.close()
        except:
            continue

if __name__ == "__main__":
        """
            Python Script Syntax: py* (python, python3, py -- depending on system) wikipedia-crawler.py {numberOfDocuments}
            
            Parameters: int numberofDocuments is passed as the number of wikipedia entries to scrape and write to file.
            Functionality: Writes numberOfDocuments amount of files to disk in ./data with wikipedia descriptions as content.
        """
        args = sys.argv
        if (len(args) > 2):
            raise ValueError("Illegal Arugments. Make sure command is of the form: \n\t py wikipedia-crawler.py \{numOfDocuments\}")
        docs = pullWikipediaData(int(args[-1]))
        writeToFile(docs)
