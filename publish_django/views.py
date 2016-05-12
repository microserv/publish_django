from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, Template
from pymongo import MongoClient
import requests
import json
from bson.objectid import ObjectId

mongodb_url = "mongodb://despina.128.no//IT2901"
indexer_url = "http://despina.128.no/indexer"

client = MongoClient(mongodb_url)
db = client["IT2901"]
collection = db["publishing"]

@csrf_exempt
def save_article(request):
	try:
		r = str(collection.insert_one(request.POST.dict()).inserted_id)
		try:
			requests.post("indexer_url", data = {"task" : "publishedArticle" , "articleID" : r})
		except:
			print("Could not update indexer.")
		return HttpResponse(status=204)
	except:
		return HttpResponse(status=500)

@csrf_exempt
def list(request):
	try:
		art_list = []
		for art in collection.find():
			art_list.append({"id": str(art["_id"]), "title": art["title"], "description": art["description"]})
		return HttpResponse(json.dumps({"list":art_list}))
	except:
		return HttpResponse(status=500)

@csrf_exempt
def article(request):
	try:
		id = request.path[-24:]
		doc = collection.find_one({'_id': ObjectId(id)})
		return render(request, "article.html", Context({"title": doc["title"], "body": doc["article"]}));
	except:
		return HttpResponse(status=500)

@csrf_exempt
def article_json(request):
	try:
		if (request.method == "GET"):
			id = request.path[-24:]
			doc = collection.find_one({'_id': ObjectId(id)})
			res = {"title": doc["title"], "description": doc["description"], "article": doc["article"], "tags": doc["tags"], "_id": doc["_id"]}
			return HttpResponse(json.dumps(res))
		elif (request.method == "DELETE"):
			id = request.path[-24:]
			collection.delete_one({'_id': ObjectId(id)})
			try:
				requests.post("indexer_url", data = {"task" : "removedArticle" , "articleID" : id})
			except:
				print("Could not update indexer.")
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=500)
	except:
		return HttpResponse(status=500)
