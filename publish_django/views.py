from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, Template
from pymongo import MongoClient
import requests
import json
from bson.objectid import ObjectId


NODE_ADDR = "http://127.0.0.1:9001"
DB_NAME = "IT2901"

def get_collection(collection_name):
	mongodb_url = "mongodb://" + get_service_ip("mongodb") + "/" + DB_NAME

	client = MongoClient(mongodb_url)
	db = client[DB_NAME]
	return db[collection_name]

def get_service_ip(service_name):
	response_as_json = None
	r = requests.get(NODE_ADDR + "/" + service_name)

	return json.loads(r.text)


@csrf_exempt
def success(request):
	return HttpResponse(status=200)

@csrf_exempt
def save_article(request):
	collection = get_collection("publishing")
	try:
		r = str(collection.insert_one(request.POST.dict()).inserted_id)
		try:
			indexer_url = "http://" + get_service_ip("indexer")
			requests.post("indexer_url", data = {"task" : "publishedArticle" , "articleID" : r})
		except:
			print("Could not update indexer.")
		return HttpResponse(status=204)
	except:
		return HttpResponse(status=500)

@csrf_exempt
def list(request):
	collection = get_collection("publishing")
	try:
		art_list = []
		for art in collection.find():
			art_list.append({"id": str(art["_id"]), "title": art["title"], "description": art["description"]})
		return HttpResponse(json.dumps({"list":art_list}))
	except:
		return HttpResponse(status=500)

@csrf_exempt
def article(request):
	collection = get_collection("publishing")
	try:
		id = request.path[-24:]
		doc = collection.find_one({'_id': ObjectId(id)})
		return render(request, "article.html", Context({"title": doc["title"], "body": doc["article"]}));
	except:
		return HttpResponse(status=500)

@csrf_exempt
def article_json(request):
	collection = get_collection("publishing")
	try:
		if (request.method == "GET"):
			id = request.path[-24:]
			doc = collection.find_one({'_id': ObjectId(id)})
			res = {"title": doc["title"], "description": doc["description"], "article": doc["article"], "tags": doc["tags"], "_id": str(doc["_id"])}
			return HttpResponse(json.dumps(res))
		elif (request.method == "DELETE"):
			id = request.path[-24:]
			collection.delete_one({'_id': ObjectId(id)})
			try:
				indexer_url = "http://" + get_service_ip("indexer")
				requests.post("indexer_url", data = {"task" : "removedArticle" , "articleID" : id})
			except:
				print("Could not update indexer.")
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=500)
	except:
		return HttpResponse(status=500)
