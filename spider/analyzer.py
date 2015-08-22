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

def testKeywords ():

	tags = jieba.analyse.textrank("目前可收托12歲以下兒童4人。 依於衛生福利部103年9月15日以部授家字第1030900692號令訂定發布之「居家式托育服務提供者登記及管理辦法」規定，自103年12月1日起，收托人數說明如下： 1.每1托育人員照顧半日、日間、延長或臨時托育兒童至多4人，其中未滿2歲兒童至多2人。 2.每1托育人員照顧全日或夜間托育兒童至多2人。 3.每1托育人員照顧全日或夜間托育兒童1人者，得增加收托半日、日間、延長或臨時托育之兒童至多2人，其中未滿2歲兒童至多2人。 4.每1托育人員照顧夜間托育2歲以上兒童2人者，得增加收托半日、日間、延長或臨時托育之兒童至多1人。 5.2名以上托育人員於同一處所共同照顧兒童至多4人，其中全日或夜間托育兒童至多2人。 收托人數，應以托育人員托育服務時間實際照顧兒童數計算，並包括其六歲以下之子女、受其監護及三親等內兒童。 聯合收托育者，應就收托之兒童分配主要照顧人。,兒童托育,新生兒,兒童,保母,托育,QA", topK=5, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v')) 
	print(tags)

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

superMerger();

