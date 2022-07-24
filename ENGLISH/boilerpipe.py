from bs4 import BeautifulSoup
from boilerpipe.extract import Extractor
import json
import nltk
def run_crawl(url):
	print("url:",url)
	#url="https://edition.cnn.com/2021/09/20/europe/poland-coal-mine-turow-fine-eu-intl/index.html"
	try:
		extractor = Extractor(extractor='KeepEverythingExtractor', url=url)
	except:
		return ["",""]
	extracted_html = str(extractor.getHTML())
	if len(extracted_html)==0:
		return ["",""]

	soup = BeautifulSoup(extracted_html, 'html.parser')
	# print("#######################\n",soup)
	if soup.find("h1")==None:
		return ["",""]
	title=soup.find("h1").text
	print("#######################\n:",title)

	try:
		extractor_clean = Extractor(extractor='ArticleExtractor', url=url)
	except:
		return ["",""]
	content = str(extractor_clean.getText())
	# print("#######################\n:",content)
	
	
	
	sent_text = nltk.sent_tokenize(content)
	if len(title)==0 or len(sent_text)<=5 or "?" in title.lower() or "why" in title.lower() or "how" in title.lower():
		return ["",""]
	return [content,title]


content,title=run_crawl(url)


# def get_event_name():
# 	import os
# 	base_path="遗漏数据汇总3"
# 	g=os.walk(base_path)
# 	event_type=[]
# 	for path,dir_list,file_list in g:
# 		for file_name in file_list:
# 			if "csv" in file_name:
# 				event_type.append(file_name[:-4])
# 	print(event_type)

# def get_original_news(event):
# 	data=open("遗漏数据汇总3/"+event+".csv").readlines()
# 	f=open("遗漏数据汇总3/"+event+"0.txt","w")
# 	print("event name:",event)
# 	for index,url in enumerate(data):
# 		url=url.strip()
# 		print("index:",str(index))
# 		content,title=run_crawl(url)
# 		if len(content)!=0:
# 			oo=json.dumps({"event":title,"content":content,"url":url})
# 			f.write(oo+"\n")
# 	f.close()

# #Famous Person-Sick', 
# #event_type=['Tsunamis', 'Famous Person-CommitCrime-Release', 'Famous Person-CommitCrime-Sentence', 'Mass Poision', 'Disease Outbreaks', 'Marriage', 'Tear Up Agreement', 'Divorce', 'Financial Aid', 'Organization Merge', 'Insect', 'Bank Robbery', 'Withdraw from an organization', 'Financial Crisis', 'Volcano Eruption', 'Gas explosion', 'Break historical records', 'New wonders in nature', 'Organization Established', 'New achievements in aerospace', 'famine', 'Shipwreck', 'Organization Fine', 'Mudslides', 'Organization Closed', 'Sign Agreement', 'Road Crash', 'Drought', 'Diplomatic Visit', 'Awards ceremony', 'Military Excercise', 'New archeological discoveries', 'Famous Person-Give a speech', 'Environment Pollution', 'Mine Collapses']
# event_type=["Regime Change","Famous Person - Recovered","Famous People-CommitCrime-Investigate"]
# for event in event_type:
# 	get_original_news(event)

# # get_original_news("Famous Person-Sick")



