import sys
import os
import http.cookiejar
import json
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup

#declare directory name for images
rootdir = "pictures"

#cook some soup
query = sys.argv[1].split()
query ='+'.join(query)
url = "http://www.bing.com/images/search?q=" + query + "&FORM=QBIR"
header={'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"}
soup = BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url, headers=header)), 'html.parser')

#store image links in list
imageLinks = []
for data in soup.find_all("a",{"class":"iusc"}):
    json_data = json.loads(data["m"])
    img_link = json_data["murl"]
    img_link_b = json_data["turl"]
    img_name = urllib.parse.urlsplit(img_link).path.split("/")[-1]
    imageLinks.append((img_name, img_link_b, img_link))

#create the root and sub directories
if not os.path.exists(rootdir):
    os.mkdir(rootdir)
rootdir = os.path.join(rootdir, query.split()[0])
if not os.path.exists(rootdir):
    os.mkdir(rootdir)

#download the images
for i, (img_name, img_link_b, img_link) in enumerate(imageLinks):
    raw_img = urllib.request.urlopen(img_link_b).read()
    cntr = len([i for i in os.listdir(rootdir) if img_name in i]) + 1
    f = open(os.path.join(rootdir, img_name), 'wb')
    f.write(raw_img)
    f.close()
