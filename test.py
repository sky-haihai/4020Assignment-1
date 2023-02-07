import xml.etree.ElementTree as ET
import urllib.request as ulreq
import urllib.parse as ulparse
from textwrap import indent
import time
from xml.dom import minidom
from textwrap import indent
import os 

#ESEARCH_URL='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?'
#
#params={'db':'pubmed','term':'Hyperglycemia contributes insulin resistance in hepatic and adipose tissue but not skeletal muscle of ZDF rats.','field':'title'}
#quotes=ulparse.urlencode(params)
#
#finalUrl=ESEARCH_URL+quotes
#print(finalUrl)
#locker=True
#while(locker):
#  try:
#    responseStr=ulreq.urlopen(finalUrl).read()
#    locker=False
#  except:
#    print('an error occured')
#    locker=True

#responseStr=ulreq.urlopen('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi').read()
#responseRoot=ET.fromstring(responseStr)
#roughStr=ET.tostring(responseRoot,'utf-8')
#prettyStr=minidom.parseString(roughStr).toprettyxml(indent='  ')
#
#save_path_file='res/databaseInfo.xml'
#with open(save_path_file, "w") as f:
#  f.write(prettyStr)

print(12%12)