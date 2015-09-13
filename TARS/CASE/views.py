from django.shortcuts import render
import cluster
import json
from django.http import HttpResponse

def sendQuestion(request):
	#print(request)
	#data = {}
	data = cluster.doKMeans(request.POST['data'])

	return HttpResponse(json.dumps(data), content_type="application/json")

def test(request):
	return HttpResponse('<form method="POST" action="/case/sendQuestion"><input type="text" name="data"></input><input type="submit"></input></form>')
