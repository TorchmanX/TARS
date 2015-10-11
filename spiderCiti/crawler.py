# coding=UTF8
import requests
from pyquery import PyQuery as pq
import urllib
import json
import unirest
import re
import arff
import codecs
import itertools
#import urllib2
# encoding=utf8  
import sys

reload(sys)  
sys.setdefaultencoding('utf8')

#article
class Article:
	def __init__(self):
		self.ContentID = None
		self.Category = []
		self.Title = None
		self.Content = None
		self.URL = None

	def toJSON(self):
		return json.dumps({"ContentID": self.ContentID, "Category": self.Category, "Title": self.Title, "Content": self.Content, "URL": self.URL})

def getArchivesIDList(page):
	url = 'http://1999.taipei.gov.tw/TCGGetSearch.ASPX?CategoryID=0&CategoryType=Key&KeyList=&PageNo='+str(page)+'&SortOrder=CreateDate%20DESC,%20Subject&adv=N'
	dom = pq(url=url);
	ArchivesIDList = [];
	for a in dom.items('a'):
		ArchivesIDList.append(int(a.attr('href').split('\'')[1]));
	return ArchivesIDList;

def getArchivesIDListFromARFF():
	start = int(sys.argv[1])
	end = int(sys.argv[2])
	f = codecs.open('article_merged_2.arff', 'r', encoding='utf8')
	span = 0
	ArticleList = []
	for index, l in enumerate(f):
		if(l[0] == '@'):
			span = span + 1
			continue
		elif(index >= start + span and index < end + span):
			l = l.split(',')
			ID = l[0].replace('"', '')
			a = getArticle(ID)
			if(a == False):
				continue
			ArticleList.append(a.toList())
		else:
			continue
	arff.dump('article_v2_'+str(start)+'_'+str(end)+'.arff', ArticleList, relation="article", names=['ArchivesID', 'Category', 'Department', 'ReadCount', 'Title', 'Content', 'Glossary'])

def getArticle(ContentID):
	try:
		url = 'https://online.citi.com/US/JRS/helpcenter/getHelpContent.do?contentID='+ContentID+'&contentType=help_item='
		dom = pq(url=url)
		a = Article()
		a.ContentID = ContentID
		a.Category = [dom.find('.breadcrumb').find('a').eq(2).text(), dom.find('.breadcrumb').find('a').eq(3).text()]
		a.Title = dom.find('.help_title').text()
		a.Content = re.sub(r'[ 　\t\r\n\"]', '',dom.find('#contentDiv').find('ol').text())
		a.URL = url
		print(a.toJSON);
		return a;
	except:
		return False

def getArticleList():
	ArticleList = []
	for i in range(int(sys.argv[1]), int(sys.argv[2])) :
		print('page '+str(i));
		ArchivesIDList = getArchivesIDList(i)
		for ID in ArchivesIDList:
			a = getArticle(ID)
			ArticleList.append(a.toList())

		arff.dump('article_'+str(i)+'.arff', ArticleList, relation="article", names=['ArchivesID', 'Category', 'Department', 'ReadCount', 'Title', 'Content', 'Glossary'])


getArticle('StepsToTakeWhenReceiveNewCard')
