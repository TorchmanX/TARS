from django.shortcuts import render
import cooper
import json
from django.http import HttpResponse

# Create your views here.

def sendQuestion(request):
	data = {}
	data['Category'] = cooper.getCategory(request.POST['question'])
	data['Deps'] = cooper.getDepsbyCategory(data['Category'])

	return HttpResponse(json.dumps(data), content_type="application/json")
