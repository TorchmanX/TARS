# coding=UTF8
import arff
import codecs
import jieba.analyse
import itertools
# encoding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')
def mergeArticleArff ():
	ArticleArffList = []
	duplicate_id = []
	for i in range(int(sys.argv[1]), int(sys.argv[2])) :
		print('page '+str(i))
		f = codecs.open('article_'+str(i)+'.arff', 'r', encoding='utf8')
		for l in f:
			if (l[0] == '@'): 
				continue
			try:
				l = l.split(',')
				if(len(l) < 5 or l[0].isnumeric() == False):
					continue
				if(l[0] in duplicate_id):
					continue
				duplicate_id.append(l[0])
				ArticleArffList.append('"'+('","').join(l[0:5])+'"\n')
			except:
				continue

	#arff.dump('article_merged.arff', ArticleArffList, relation="article", names=['ArchivesID', 'Category', 'Department', 'ReadCount', 'Title'])
	f = codecs.open('archive/article_merged.arff', 'w', encoding='utf8')
	f.writelines(['@relation article\n','@attribute ArchivesID string\n','@attribute Category string\n','@attribute Department string\n','@attribute ReadCount string\n','@attribute Title string\n','@data\n'])
	#print(ArticleArffList)
	f.writelines(ArticleArffList)

def getKeywords ():
	f = codecs.open('article_merged.arff', 'r', encoding='utf8')
	KeywordList = []
	for l in f:
		title = l[4]
		tags = jieba.analyse.textrank(title, topK=5, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v')) 
		print(l[4])
		print(tags)

def getCategoryList ():
	CategoryList = dict()
	f = codecs.open('article_merged_2.arff', 'r', encoding='utf8')
	for row in f:
		if(row[0]=='@'): continue
		c_list = row.split(',')[1].replace('"', '').split(';')
		for c in c_list:
			if(c != ''):
				try:
					CategoryList[c] = CategoryList[c] + 1
				except:
					CategoryList[c] = 1

	f = codecs.open('category.csv', 'w', encoding='utf8')
	f.write('"category", "freq"\n')
	for c, freq in CategoryList.items():
		f.write('"'+c+'",'+str(freq)+'\n')
	f.close()

def analyzeKeywords():
	
	f = codecs.open('category.csv', 'r', encoding='utf8')
	category_list = dict()
	i=0
	for l in f:
		l = l.split(',')
		if(l[0] == '"category"'):continue
		c = l[0].replace('"', '')
		if(c=="''" or c==""):
			c = u"其他"
		category_list[c] = i
		i = i+1

	start = int(sys.argv[1])
	end = int(sys.argv[2])
	f = codecs.open('article_v2_'+str(start)+'_'+str(end)+'.arff', 'r', encoding='utf8')
	keyword_list = dict()

	for l in f:
		if(l[0] == '@'): continue

		row = l.split(',')
		print(row[4])

		sentence = ','.join(row[4:6])
		category = row[1].replace('"', '').split(';')
		keywords = jieba.analyse.textrank(sentence, topK=5, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'))
		print(keywords)
		for k in keywords:
			for c in category:
				if(c==""):
					c = u"其他"
				if(c not in category_list):
					continue
				try:
					keyword_list[k[0]][category_list[c]] += k[1]
				except:
					keyword_list[k[0]] = dict()
					keyword_list[k[0]][category_list[c]] = k[1]

		f = codecs.open('keyword_list_'+str(start)+'_'+str(end)+'.csv', 'w', encoding='utf8')
		f.write('"category","'+'","'.join(category_list)+'"\n')

		for key, arr in keyword_list.items():
			row = [key]
			for i in range(0, len(category_list)):
				try:
					row.append(str(arr[i]))
				except:
					row.append("0")

			f.write('"'+'","'.join(row)+'"\n')
		f.close()


def superMerger ():
	ArticleArffList = []
	duplicate_id = []
	collect = False
	ID = 0
	Category = None
	Department = None
	ReadCount = 0
	Title = None
	Content = None

	for i in range(int(sys.argv[1]), int(sys.argv[2])) :
		print('page '+str(i))
		f = codecs.open('article_'+str(i)+'.arff', 'r', encoding='utf8')
		for l in f:
			if (l[0] == '@'): 
				continue

			if (l[0:5].isnumeric()):
				collect = True
			else:
				collect = False

			if(collect):
				if(ID != 0):
					ArticleArffList.append('"'+ID+'", "'+Category+'", "'+Department+'", "'+ReadCount+'", "'+Title+'", "'+Content+'"\n')
					duplicate_id.append(ID)
				l = l.replace(' ', '').replace('"', '').replace('\n', '')
				l = l.split(',');
				if(l[0] in duplicate_id):
					continue

				ID = l[0]
				Category = l[1]
				Department = l[2]
				ReadCount = l[3]
				Title = l[4]
				Content = l[5:]
			else:
				Content += l.replace(' ', '').replace('"', '').replace('\n', '').replace(',', '')

	f = codecs.open('article_merged.arff', 'w', encoding='utf8')
	f.writelines(['@relation article\n','@attribute ArchivesID integer\n','@attribute Category string\n','@attribute Department string\n','@attribute ReadCount integer\n','@attribute Title string\n', '@attribute Content string\n','@data\n'])
	#print(ArticleArffList)
	f.writelines(ArticleArffList)

analyzeKeywords();

