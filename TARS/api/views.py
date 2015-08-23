from django.shortcuts import render
import cooper
import json
import operator
from django.http import HttpResponse

# Create your views here.

def sendQuestion(request):
	data = {}
	cate = cooper.getCategory(request.POST['question'])
	tmp = []
	data['Category'] = []
	for c in cate:
		tmp += cooper.getDepsbyCategory(c[0])
		data['Category'].append(c[0]+1)
	tmp2 = {}
	for d in tmp:
		tmp2[d[0]] = d[1]
	deps = sorted(tmp2.items(), key=operator.itemgetter(1), reverse=True)[0:10]
	data['Deps'] = []
	for d in deps:
		data['Deps'].append(int(d[0]))
	return HttpResponse(json.dumps(data), content_type="application/json")

def test(request):
	return HttpResponse('<form method="POST" action="/api/sendQuestion"><input type="text" name="question"></input><input type="submit"></input></form>')

	#return

