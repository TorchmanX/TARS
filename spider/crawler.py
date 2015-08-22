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
		self.ArchivesID = 0
		self.Category = None
		self.Department = None
		self.ReadCount = 0
		self.Title = None 
		self.Content = None
		self.Glossary = None

	def toList(self):
		return ['"'+self.ArchivesID+'"', '"'+self.Category+'"', '"'+self.Department+'"', '"'+self.ReadCount+'"', '"'+self.Title+'"', '"'+self.Content+'"', '"'+self.Glossary+'"']

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
			span++
			continue
		if(index >= start + span && index < end + span):
			l = l.split(',')
			ID = l.replace('"')
			a = getArticle(ID)
			ArticleList.append(a.toList())
	arff.dump('article_v2_'+str(start)+'_'+str(end)+'.arff', ArticleList, relation="article", names=['ArchivesID', 'Category', 'Department', 'ReadCount', 'Title', 'Content', 'Glossary'])

def getArticle(ID):
	url = 'http://1999.taipei.gov.tw/TCGGetFAQ.ASPX?ArchivesID='+str(ID)
	dom = pq(url=url)
	a = Article()
	a.ArchivesID = int(ID)
	a.Category = dom.find('#Label1').text()
	a.Department = dom.find('#Label2').text()
	a.ReadCount = int(dom.find('#Label4').text())
	a.Title = dom.find('#Label5').text()
	a.Content = re.escape(dom.find('#Label6').text())
	a.Glossary = re.escape(dom.find('#Label7').text())
	print(str(ID)+' Title: '+a.Title);
	return a;

def getArticleList():
	ArticleList = []
	for i in range(int(sys.argv[1]), int(sys.argv[2])) :
		print('page '+str(i));
		ArchivesIDList = getArchivesIDList(i)
		for ID in ArchivesIDList:
			a = getArticle(ID)
			ArticleList.append(a.toList())

		arff.dump('article_'+str(i)+'.arff', ArticleList, relation="article", names=['ArchivesID', 'Category', 'Department', 'ReadCount', 'Title', 'Content', 'Glossary'])


getArchivesIDListFromARFF();
