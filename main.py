import xml.etree.ElementTree as ET
import urllib.request as ulreq
import urllib.parse as ulparse
from textwrap import indent
import time
from xml.dom import minidom
from textwrap import indent
import os 

GROUP_NUM=1 #define group number
LIMITER=10  #save time when debugging


#1. Parse XML/ Extract Article Titles 
tree=ET.parse("res/4020a1-datasets.xml")
root=tree.getroot()

titles=[]
for articleBody in root.findall('PubmedArticle'):
  article=articleBody[0].find('Article')
  title=article.find('ArticleTitle').text
  titles.append(title)


#2. Send Url Request to PubMed Server
eSearchUrl='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?'
eSpellingUrl='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/espell.fcgi?'

outputRoot=ET.Element('PubmedArticleSet')

for title in titles:
  if(LIMITER<=0):
    break

  #original title
  params={'db':'pubmed','term':title}
  quotes=ulparse.urlencode(params)

  #corrected title
  spellingStr=ulreq.urlopen(eSpellingUrl+quotes).read()
  spellingRoot=ET.fromstring(spellingStr);
  correctedTitle=spellingRoot.find('CorrectedQuery').text

  #use the new title as search quotes
  params={'db':'pubmed','term':correctedTitle}
  quotes=ulparse.urlencode(params)

  responseStr=ulreq.urlopen(eSearchUrl+quotes).read()
  time.sleep(1)
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