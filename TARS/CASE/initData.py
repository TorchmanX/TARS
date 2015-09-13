import json
import codecs
import random
import sys

def initUser():
	f = codecs.open('../data/user.json', 'w', encoding='utf8')
	jsonData = { 'USERS': []}
	for i in range(1, int(sys.argv[1])+1):
		temp = {}
		for j in range(1, int(sys.argv[2])+1):
			temp[str(j)] = random.randint(0, 3) #0 = None, 1 = negative, 2 = neutral, 3 = positive

		jsonData['USERS'].append({ 
		'UID': str(100+i),
		'V_ANS':{
			'iphone6s': temp
			}
		})

	f.write(json.dumps(jsonData))
	f.close()

initUser()
