from django.shortcuts import render
import cluster
import json
from django.http import HttpResponse

def sendQuestion(request):
	data = {}
	data['sphereList'] = cluster.doKMeans()

	return HttpResponse(json.dumps(data), content_type="application/json")
