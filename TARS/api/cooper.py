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
	category_list = []
	ref_keyword_list = []
	pos_list = ['ns', 'n', 'vn', 'v']
	for word, tag in seg_list:
		if(tag in pos_list):
			keyword_list.append(word)

	f = codecs.open('data/keyword_list_0_1000.csv', 'r', encoding='utf8')
	attr_flag = True
	for l in f:
		if(attr_flag):
			attr_flag = False
			continue

		l = l.replace('"', '').split(',')
		if( l[0] in keyword_list):
			print(l[0])
			if(category_list == []):
				for i in range(1, len(l)):
					category_list.append(float(l[i]))
			else:
				for i in range(0, len(category_list)):
					category_list[i] = float(l[i+1]) + float(category_list[i])

	outcome = -1
	val = 0
	for i in range(0, len(category_list)):
		if(category_list[i] > val):
			outcome = i
			val = category_list[i]
	print(keyword_list)
	return outcome

def getDepsbyCategory(cate_id):
	attr_flag = True
	dep_list = dict()
	index = int(cate_id)+1
	f = codecs.open('data/dep_cate_list.csv', 'r', encoding='utf8')
	for l in f:
		if(attr_flag):
			attr_flag = False
			continue

		l = l.replace('"', '').split(',')

		if(int(l[index]) > 0):
			dep_list[l[0]] = int(l[index])

	sorted_outcome = sorted(dep_list.items(), key=operator.itemgetter(1), reverse=True)

	#keylist = dep_list.keys()
	#keylist.sort(reverse=True)
	'''
	for key in keylist:
		outcome.append(dep_list[key])
	'''
	return sorted_outcome
