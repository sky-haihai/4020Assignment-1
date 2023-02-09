import xml.etree.ElementTree as ET
import urllib.request as ulreq
import urllib.parse as ulparse
from textwrap import indent
import time
from xml.dom import minidom
from textwrap import indent
import os 

GROUP_NUM=99 #define group number
LIMITER=6000  #save time when debugging
ESPELL_URL='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/espell.fcgi?'
ESEARCH_URL='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?'
ECITMATCH_URL='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/ecitmatch.cgi?'
API_KEY='42566828cae548720b64e51c7d2f4754e608'

def get_request_str(url):
  locker=True
  while(locker):
    try:
      responseStr=ulreq.urlopen(url).read()
      locker=False
      return responseStr
    except:
      print('an url request error occured')
      locker=True

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

def appendChild(outputRoot,id,name):
  articleElement=ET.SubElement(outputRoot,'PubmedArticle')
  idElement=ET.SubElement(articleElement,'PMID')
  idElement.text=id
  titleElement=ET.SubElement(articleElement,'ArticleTitle')
  titleElement.text=name

#1. Parse XML/ Extract Article Titles 
tree=ET.parse("res/4020a1-datasets.xml")
root=tree.getroot()

queryTuples=[]
for articleBody in root.findall('PubmedArticle'):
  article=articleBody.find('MedlineCitation').find('Article')
  title=article.find('ArticleTitle').text
  print(title)
  journal=article.find('Journal')

  journalTitle='null'
  try:
    journalTitle=journal.find('Title').text
  except:
    journalTitle='null'

  journalIssue=journal.find('JournalIssue')
  journalYear=journalIssue.find('PubDate').find('Year').text
  journalVolume=journalIssue.find('Volume').text
  firstPage=article.find('Pagination').find('MedlinePgn').text
  
  authorName='null'
  author=article
  try:
    author=article.find('AuthorList').find('Author')
    authorName=author.find('LastName').text+' '+author.find('ForeName').text
  except:
    authorName='null'
  
  tuple=(title,journalTitle,journalYear,journalVolume,firstPage,authorName)
  queryTuples.append(tuple)


#2. Send Url Request to PubMed Server
outputRoot=ET.Element('PubmedArticleSet')

for tuple in queryTuples:
  if(LIMITER<=0):
    break
  LIMITER-=1

  #if starts with 're:' send a ecitmatch request
  if(tuple[0].startswith('Re: \"')):
    print('this is a ecitmatch')
    citStr=tuple[1]+'|'+tuple[2]+'|'+tuple[3]+'|'+tuple[4]+'|'+tuple[5]+'|'
    params={'db':'pubmed','retmode':'xml','bdata':citStr,'api_key':API_KEY}
    quotes=ulparse.urlencode(params)
    url=ECITMATCH_URL+quotes
    responseBytes=get_request_str(url)
    components=responseBytes.decode('utf-8').split("|")
    id=components[len(components)-1]
    print(id)

    appendChild(outputRoot,id,tuple[0])
    continue
 
  #normal titles
  params={'db':'pubmed','term':'\"'+tuple[0]+'\"[Title:~2]','api_key':API_KEY}
  quotes=ulparse.urlencode(params)

  finalUrl=ESEARCH_URL+quotes

  responseStr=get_request_str(finalUrl)
  #time.sleep(0.2)
  responseRoot=ET.fromstring(responseStr)

  #if has result use the first one
  count=0
  try:
    count=int(responseRoot.find('Count').text)
  except:
    print(responseRoot.tag)
    appendChild(outputRoot,'00000000',tuple[0])
    continue

  print(f'{LIMITER} count:{count}')

  if(count>0):
    id=responseRoot.find('IdList')[0].text
    appendChild(outputRoot,id,tuple[0])
  else:
    #try again using a title suggested by espell api
    espellParams={'db':'pubmed','term':tuple[0],'api_key':API_KEY}
    espellQuotes=ulparse.urlencode(espellParams)
    spellingUrl=ESPELL_URL+espellQuotes
    spellingStr=get_request_str(spellingUrl)
    spellingRoot=ET.fromstring(spellingStr)
    correctedTitle=spellingRoot.find('CorrectedQuery').text
    print('using espelling: '+correctedTitle)

    params={'db':'pubmed','term':correctedTitle,'field':'title','api_key':API_KEY}
    quotes=ulparse.urlencode(params)

    finalUrl=ESEARCH_URL+quotes
    #print(finalUrl)

    responseStr=get_request_str(finalUrl)
    responseRoot=ET.fromstring(responseStr)
    count=int(responseRoot.find('Count').text)
    if(count>0):
      id=responseRoot.find('IdList')[0].text
      appendChild(outputRoot,id,tuple[0])
    else:
      print('no results: '+tuple[0])
      appendChild(outputRoot,'00000000',tuple[0])

#3. Write to XML File
#outputTree=ET.ElementTree(outputRoot)
roughStr=ET.tostring(outputRoot,'utf-8')
prettyStr=minidom.parseString(roughStr).toprettyxml(indent='  ')

save_path_file='res/group'+str(GROUP_NUM)+'_result.xml'
with open(save_path_file, "w") as f:
  f.write(prettyStr)