import xml.etree.ElementTree as ET
import urllib.request as ulreq
import urllib.parse as ulparse
from textwrap import indent
import time
from xml.dom import minidom
from textwrap import indent
import os 

GROUP_NUM=1 #define group number
LIMITER=500  #save time when debugging
ESEARCH_URL='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?'
API_KEY='42566828cae548720b64e51c7d2f4754e608'

def month2num(month):
  match month:
    case 'Jan':
      return 1
    case 'Feb':
      return 2
    case 'Mar':
      return 3
    case 'Apr':
      return 4
    case 'May':
      return 5
    case 'Jun':
      return 6
    case 'Jul':
      return 7
    case 'Aug':
      return 8
    case 'Sep':
      return 9
    case 'Sept':
      return 9
    case 'Oct':
      return 10
    case 'Nov':
      return 11
    case 'Dec':
      return 12
    case _:
      raise Exception(f'Month:{month} Not Existed')


#1. Parse XML/ Extract Article Titles 
tree=ET.parse("res/4020a1-datasets.xml")
root=tree.getroot()

queryTuples=[]
for articleBody in root.findall('PubmedArticle'):
  article=articleBody.find('MedlineCitation').find('Article')
  title=article.find('ArticleTitle').text
  pdate=article.find('Journal').find('JournalIssue').find('PubDate')
  year=int(pdate.find('Year').text)
  month=month2num(pdate.find('Month').text)

  minDate=(year,month,1)
  maxDate=(year,month+1,1)
  if(maxDate[1]==13):
    maxDate=(year+1,1,1)

  tuple=(title,minDate,maxDate)
  queryTuples.append(tuple)


#2. Send Url Request to PubMed Server
outputRoot=ET.Element('PubmedArticleSet')

for tuple in queryTuples:
  #print(tuple[0])
  if(LIMITER<=0):
    break

  #original title
  minDate=f'{tuple[1][0]}/{tuple[1][1]}/{tuple[1][2]}'
  maxDate=f'{tuple[2][0]}/{tuple[2][1]}/{tuple[2][2]}'
  params={'db':'pubmed','term':tuple[0],'field':'title','datetype':'pdat','mindate':minDate,'maxdate':maxDate,'api_key':API_KEY}
  quotes=ulparse.urlencode(params)

  finalUrl=ESEARCH_URL+quotes
  print(finalUrl)

  responseStr=ulreq.urlopen(finalUrl).read()
  #locker=True
  #while(locker):
  #  try:
  #    responseStr=ulreq.urlopen(finalUrl).read()
  #    locker=False
  #  except:
  #    print('an error occured')
  #    locker=True

  #time.sleep(0.2)
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
    titleElement.text=tuple[0]
    #print(titleElement.text)

  else:
    #append debug child
    articleElement=ET.SubElement(outputRoot,'PubmedArticle')
    idElement=ET.SubElement(articleElement,'PMID')
    idElement.text='00000000'
    titleElement=ET.SubElement(articleElement,'ArticleTitle')
    titleElement.text=tuple[0]
    #print(titleElement.text)

  LIMITER-=1

#3. Write to XML File
#outputTree=ET.ElementTree(outputRoot)

roughStr=ET.tostring(outputRoot,'utf-8')
prettyStr=minidom.parseString(roughStr).toprettyxml(indent='  ')

save_path_file='res/group'+str(GROUP_NUM)+'_result.xml'
with open(save_path_file, "w") as f:
  f.write(prettyStr)