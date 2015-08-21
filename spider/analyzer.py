# coding=UTF8
import arff
import codecs
# encoding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')
def mergeArticleArff ():
	ArticleArffList = []
	for i in range(0, 4) :
		print('page '+str(i))
		f = codecs.open('article_'+str(i)+'.arff', 'r', encoding='utf8')
		for l in f:
			if (l[0] == '@'): 
				continue
			try:
				l = l.split(',')
				if(len(l) < 5):
					continue
				ArticleArffList.append('"'+('","').join(l[0:5])+'"\n')
			except:
				continue

	#arff.dump('article_merged.arff', ArticleArffList, relation="article", names=['ArchivesID', 'Category', 'Department', 'ReadCount', 'Title'])
	f = codecs.open('article_merged.arff', 'w', encoding='utf8')
	f.writelines(['@relation article\n','@attribute ArchivesID string\n','@attribute Category string\n','@attribute Department string\n','@attribute ReadCount string\n','@attribute Title string\n','@data\n'])
	print(ArticleArffList)
	f.writelines(ArticleArffList)

mergeArticleArff();