from numpy import array
from scipy.cluster.vq import vq, kmeans2, whiten
import json
import math
import operator
from sklearn.tree import DecisionTreeRegressor
import sys

def doKMeans(filename):
	'''
	with open(filename) as data_file:    
		data = json.load(data_file)
	'''
	#data = json.load(filename)
	data = filename
	vertex_matrix = []
	UID = []
	print(data)
	for user in data["USERS"]:
		arr = []
		for VID, V_ANS in user["V_ANS"]["iphone6s"].items():
			arr.append(V_ANS)
		vertex_matrix.append(arr)
		UID.append(user["UID"])
		#print(arr)

	if(len(vertex_matrix)==1):
		vertex_matrix.append(vertex_matrix[0])
	print(vertex_matrix)

	whitened = whiten(vertex_matrix)
	k = math.floor(math.sqrt(len(vertex_matrix)/2))
	cluster = kmeans2(whitened,k, 99, 'points')

	print cluster

	centroid = []
	sorted_centroid = []
	sorted_vertex = []

	i=0
	for cen in cluster[0]:
		x = sum(cen)
		j = 0
		centroid.append(dict())
		sorted_vertex.append(list())
		sorted_centroid.append(list())
		for y in cen:
			j+=1
			centroid[i][str(j)] = y/x
		sorted_centroid[i] = sorted(centroid[i].items(), key=operator.itemgetter(1))
		for c_list in sorted_centroid[i]:
			sorted_vertex[i].append(c_list[0])
		i+=1

		#print arr
	print sorted_centroid
	print sorted_vertex

	circled_vertex = []
	
	i=0
	for arr in sorted_vertex:
		
		circled_vertex.append(list())
		j = 0
		for v in arr:
			if(j%2 == 0):
				circled_vertex[i] = circled_vertex[i] + [v]
			else:
				circled_vertex[i] = [v] + circled_vertex[i]
			j+=1
		i+=1

	print circled_vertex

	pivot = circled_vertex[0][0]

	for i in range(1, len(circled_vertex)):
		if(circled_vertex[i].index(pivot) != 0):
			circled_vertex[i] = circled_vertex[i][circled_vertex[i].index(pivot):] + circled_vertex[i][0:circled_vertex[i].index(pivot)]

	print circled_vertex

	final_vertex = []
	for i in range(0, len(circled_vertex[0])):
		vote = dict()
		for j in range(0, len(circled_vertex[0])):
			vote[str(j+1)] = 0
		for j in range(0, len(circled_vertex)):
			try:
				vote[circled_vertex[j][i]] += 1
			except:
				vote[circled_vertex[j][i]] = 1
		sorted_vote = sorted(vote.items(), key=operator.itemgetter(1))
		#sorted_vote = sorted_vote[::-1]
		for v in reversed(sorted_vote):
			if(v[0] not in final_vertex):
				final_vertex.append(v[0])
				break

	print(final_vertex)

	sphere_vertex_weight = []
	for v in final_vertex:
		sphere_vertex_weight.append(0)

	for c in cluster[1]:
		for v in final_vertex:
			sphere_vertex_weight[int(v)-1] += cluster[0][c][int(v)-1]

	total_weight = sum(sphere_vertex_weight)
	for i in range(0, len(sphere_vertex_weight)):
		sphere_vertex_weight[i] = sphere_vertex_weight[i] / total_weight


	print(sphere_vertex_weight)

	planetList = []
	for i in range(0, len(cluster[0])):
		planetList.append({"users":[]})
		planetList[i]["vertex_weight"] = []
		for v in final_vertex:
			planetList[i]["vertex_weight"].append(centroid[i][v])
	

	for i in range(0, len(cluster[1])):
		planetList[cluster[1][i]]["users"].append({"userId": UID[i]})
		#planetList[i]["users"].append({"userId": UID[cluster[1][j]]})

	

	print(planetList)
	
	
	result={
		"sphereList":[{
			"vertex": final_vertex,
			"vertex_weight": sphere_vertex_weight,
			"planetList": planetList
		}]
	}

	print(json.dumps(result))

	saveJson = {"userData":[], "userCluster":[]}
	for i in range(0, len(cluster[1])):
		arr = []
		#arr.append(UID[j])
		for j in range(0, len(vertex_matrix[i])):
			arr.append(vertex_matrix[i][j])
		#arr.append(cluster[1][i])
		saveJson["userData"].append(arr)
		saveJson["userCluster"].append(cluster[1][i])

	with open('../data/userCluster.json', 'w') as data_file:    
		data_file.write(json.dumps(saveJson))

	return result	

def doClassifier():
	with open('../data/userCluster.json') as data_file:    
		data = json.load(data_file)

	regressor = DecisionTreeRegressor()
	new_user = [1, 1, 0, 1, 0, 2, 3, 3, 2, 2, 1]

	regressor.fit(data["userData"], data["userCluster"])

	print(regressor.predict(new_user))

if(len(sys.argv) == 3):
	if(sys.argv[1] == 'local'):
		if(sys.argv[2] == 'cluster'):
			doKMeans('../data/user.json')
		elif(sys.argv[2] == 'classifier'):
			doClassifier()
	elif(sys.argv[1] == 'server'):
		if(sys.argv[2] == 'cluster'):
			doKMeans('data/user.json')
		elif(sys.argv[2] == 'classifier'):
			doClassifier()

