#!/usr/bin/env python3

from asyncio import constants
from urllib import response
from flask import Flask, make_response, redirect, request, jsonify, send_from_directory, render_template
import os, json, math
from werkzeug.utils import secure_filename

from search import main as searchMain
from ratcliff.ratcliff import ratcliff
from flask_cors import CORS, cross_origin

from jaccard_search import get_jaccardian_similarity
from collections import OrderedDict

from levDistance.levDist import *


app = Flask(__name__, static_folder = "./frontend/build" , static_url_path='', template_folder = "frontend/build")
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 10 #10 mb file max!
app.config['UPLOAD_EXTENSIONS '] = ['.txt']
CORS(app)

dictionary = set()
if os.path.exists("./data") and os.listdir("./data") != None:
    for file in os.listdir("./data"):
        f = open("./data/" + file, mode = 'r', encoding='utf8')
        words = f.read()
        words = words.split(" ")
        dictionary = dictionary | set(words)

@app.route("/search", methods = ["GET"])
# @cross_origin()
def search():
    args = request.args.to_dict()
    searchAlgo = "tfidf"
    limit = 1
    query = ""
    if args:
        if "query" not in args:
            return "Need query argument."
        elif "query" in args:
            query = args.get("query")
        if "searchAlgo" in args:
            searchAlgo = args.get("searchAlgo")
        if "limit" in args:
            limit = args.get("limit")
    else:
        return "Need at least query argument."

    listOfRelatedWords = generateEdits(query, dictionary, limit = int(limit) - 1)
    print(len(listOfRelatedWords))

    #initialize lev distance
    if os.path.exists("./data") and os.listdir("./data") != None:
        if searchAlgo == "ratcliff":
            bigresult = OrderedDict()
            """
            {
                word : [
                    (file, score)
                ]
            }
            """
            result = []
            for file in os.listdir("./data"):
                f = open("./data/" + file, mode = 'r', encoding = "utf8")
                words = f.read()
                r = ratcliff(query, words)
                result.append((file, 1.0 - float(r)))
            result.sort(key = lambda x : x[1], reverse = True)
            bigresult[query] = result[:int(limit)]

            for i in listOfRelatedWords:
                result = []
                for file in os.listdir("./data"):
                    f = open("./data/" + file, mode = 'r', encoding = "utf8")
                    words = f.read()
                    r = ratcliff(i, words)
                    result.append([file, 1.0 - float(r)])
                result.sort(key = lambda x: x[1], reverse = True)
                bigresult[i] = result[:int(limit)]

            print(bigresult)
                              
            response = jsonify({"Status": 200, "results" : bigresult})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response

        elif searchAlgo == "jaccard":
            bigresult = OrderedDict()
            result = []
            for file in os.listdir("./data"):
                f = open("./data/" + file, mode = 'r' , encoding = "utf8")
                words = f.read()
                r = ratcliff(query, words)
                result.append((file, 1.0 - float(r)))
            result.sort(key = lambda x : x[1], reverse=True)
            bigresult[query] = result[:int(limit)]

            for i in listOfRelatedWords:
                result = []
                for file in os.listdir("./data"):
                    f = open("./data/" + file, mode = 'r' , encoding = "utf8")
                    words = f.read()
                    r = get_jaccardian_similarity(words, i)
                    if len(words) > 0:
                        result.append([file, float(r) / len(words)])
                    else:
                        result.append([file, float(r)])
                for j in result:
                    if math.isinf(j[1]):
                        j[1] = 0
                result.sort(key = lambda x: x[1], reverse= True)
                bigresult[i] = result[:int(limit)]
            response = jsonify({"Status": 200, "results" : bigresult})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response

        elif searchAlgo == "tfidf": #tfidf is default
            mappings = OrderedDict()
            results = searchMain(int(limit), query)
            mappings.update({query : results})
            for i in listOfRelatedWords:
                results = searchMain(int(limit), i)
                mappings.update({i : results})

            print(mappings)
            response = jsonify({"Status": 200, "results" : mappings})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        else: #default we run all three.
            bigresult = OrderedDict()
            # result = []

            """
                Big Result Dictionary:
                word : {
                    ratcliff : []
                    tfidf : []
                    jacaard : []
                }
            """

            #do base query
            listOfRelatedWords.insert(0, query)
            for query in listOfRelatedWords:
                results_r, results_j = [],[]
                t = searchMain(int(limit), query)
                for file in os.listdir("./data"):
                    f = open("./data/" + file, mode = 'r' , encoding = "utf8")
                    words = f.read()
                    r = ratcliff(query, words)
                    j = get_jaccardian_similarity(words, query)
                    results_r.append([file, 1.0 - float(r)])
                    if len(words) > 0:
                        results_j.append([file, float(j) / len(words)])
                    else:
                        results_j.append([file, float(j)])
                for j in results_j:
                    if math.isinf(j[1]):
                        j[1] = 0

                results_j.sort(key = lambda x : x[1], reverse = True)
                results_r.sort(key = lambda x : x[1], reverse = True)

                bigresult[query] = {
                    "ratcliff" : results_r[:int(limit)],
                    "tfidf" : t,
                    "jaccard" : results_j[:int(limit)]
                }
            print(bigresult)
            response = jsonify({"Status": 200, "results" : bigresult})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
            # result.sort(key = lambda x : x[1], reverse=True)
            # bigresult[query] = result[:int(limit)]





    else:
        response = jsonify({"Status" : 400, "Error" : "No Files Uploaded"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


@app.route("/uploadDocuments", methods =["POST"])
# @cross_origin()
def upload():
    try:
        file_uploads = request.files
        print(file_uploads)
        if not os.path.isdir("./data"):
            os.mkdir(os.path.join(os.getcwd(), 'data')) 
        for fileName in file_uploads:
            print(fileName, file_uploads[fileName])
            if fileName != '':
                fileNameSecured = secure_filename(fileName)
                file_uploads[fileName].save("./data/" + fileNameSecured)
        
        response = jsonify({"Status" : 200})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        print(e)
        response = jsonify({"Status" : 400, "Error" : str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.route("/currentFiles", methods = ["GET"])
# @cross_origin()
def currentFiles():
    if not os.path.isdir("./data") or os.listdir("./data") == []:
        return make_response(jsonify({"response" : "No Files!"}), 400)
    
    return make_response(jsonify({"response" : os.listdir("./data")}))

@app.route("/", methods = ["GET"])
def test():
    # return render_template("index.html")
    # return app.send_static_file("./index.html")
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    # app.run()
    app.run(debug = True, port=os.environ.get('PORT', 80))