import xml.etree.ElementTree as ET
import urllib.request as ulreq
import urllib.parse as ulparse
from textwrap import indent
import time
from xml.dom import minidom
from textwrap import indent
import os 

GROUP_NUM=1 #define group number
LIMITER=100  #save time when debugging
ESEARCH_URL='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?'
API_KEY='42566828cae548720b64e51c7d2f4754e608'

#1. Parse XML/ Extract Article Titles 
tree=ET.parse("res/4020a1-datasets.xml")
root=tree.getroot()

titles=[]
for articleBody in root.findall('PubmedArticle'):
  article=articleBody[0].find('Article')
  title=article.find('ArticleTitle').text
  titles.append(title)


#2. Send Url Request to PubMed Server
outputRoot=ET.Element('PubmedArticleSet')

for title in titles:
  if(LIMITER<=0):
    break

  #original title
  params={'db':'pubmed','term':title,'field':'title','api_key':API_KEY}
  quotes=ulparse.urlencode(params)

  finalUrl=ESEARCH_URL+quotes
  print(finalUrl)

  responseStr=ulreq.urlopen(finalUrl).read()
  time.sleep(0.1)
  responseRoot=ET.fromstring(responseStr)

  #if has result use the first one
  count=int(responseRoot.find('Count').text)
  if(count>0):
    id=responseRoot.find('IdList')[0].text

    #append child element
    articleElement=ET.SubElement(outputRoot,'PubmedArticle')
    idElement=ET.SubElement(articleElement,'PMID')
    idElement.text=id
    titleElement=ET.SubElement(articleElement,'ArticleTitle')
    titleElement.text=title
  else:
    #append debug child
    articleElement=ET.SubElement(outputRoot,'PubmedArticle')
    idElement=ET.SubElement(articleElement,'PMID')
    idElement.text='00000000'
    titleElement=ET.SubElement(articleElement,'ArticleTitle')
    titleElement.text=title

  LIMITER-=1

#3. Write to XML File
outputTree=ET.ElementTree(outputRoot)

roughStr=ET.tostring(outputRoot,'utf-8')
prettyStr=minidom.parseString(roughStr).toprettyxml(indent='  ')

save_path_file='res/group'+str(GROUP_NUM)+'_result'
with open(save_path_file, "w") as f:
  f.write(prettyStr)