# encoding=utf8  
import jieba.posseg as pseg
import codecs
import operator
import sys

reload(sys)  
sys.setdefaultencoding('utf8')

def getCategory(sentence):
	print(sentence)
	seg_list = pseg.cut(sentence)
	keyword_list = []
	category_list = {}
	ref_keyword_list = []
	pos_list = ['ns', 'n', 'vn', 'v']
	for word, tag in seg_list:
		if(tag in pos_list):
			keyword_list.append(word)

	f = codecs.open('data/keyword_list_merged.csv', 'r', encoding='utf8')
	attr_flag = True
	for l in f:
		if(attr_flag):
			attr_flag = False
			continue

		l = l.replace('"', '').split(',')
		if( l[0] in keyword_list):
			print(l[0])
			ref_keyword_list.append(l[0])
			if(category_list == {}):
				for i in range(1, len(l)-1):
					category_list[i-1] = (float(l[i]))
			else:
				for i in range(0, len(category_list)):
					category_list[i] = float(l[i+1]) + float(category_list[i])
	'''
	outcome = -1
	val = 0
	for i in range(0, len(category_list)):
		if(category_list[i] > val):
			outcome = i
			val = category_list[i]
	
	outcome = []
	for i in range(0, 5):
		greater = 0
		greater_id = 0
		for j in range(0, len(category_list)):
			if category_list[j] > greater:
				greater = category_list[j]
				greater_id = j
		outcome.append(greater_id)
		category_list[greater_id] = 0
	'''
	sorted_outcome = sorted(category_list.items(), key=operator.itemgetter(1), reverse=True)
	print(sorted_outcome[0:5])
	outcome = {}
	outcome['category'] = sorted_outcome[0:5]
	outcome['keyword'] = ref_keyword_list
	return outcome

def getDepsbyCategory(cate_id, weight):
	attr_flag = True
	dep_list = dict()
	index = int(cate_id)+1
	if(index == 0):
		return []
	f = codecs.open('data/dep_cate_list.csv', 'r', encoding='utf8')
	i = 1
	for l in f:
		if(attr_flag):
			attr_flag = False
			continue

		l = l.replace('"', '').split(',')

		if(int(l[index]) > 0):
			dep_list[str(i)] = int(l[index]) * weight
		i += 1

	sorted_outcome = sorted(dep_list.items(), key=operator.itemgetter(1), reverse=True)

	#keylist = dep_list.keys()
	#keylist.sort(reverse=True)
	'''
	for key in keylist:
		outcome.append(dep_list[key])
	'''
	return sorted_outcome
