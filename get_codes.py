import urllib2
import urllib
import cookielib
import re
from HTMLParser import HTMLParser

def formatFileName(name = ''):
  s = name.replace("[*]", '')
  return s

def getFileName(txt):
  filename = []
  info_reg = re.compile("<legend>(.*?)</legend>", re.DOTALL)
  txt = re.search(info_reg, txt).group(1)
  info_reg = re.compile("<ul.*?>(.*)</ul>", re.DOTALL)
  txt = re.search(info_reg, txt).group(1)

  info_reg = re.compile("<li.*?>.*?<a.*?>(.*?)</a>.*?</li>", re.DOTALL)
  info_start = 0
  while True:
    res = re.search(info_reg, txt[info_start:])
    if res == None: break
    temptxt = res.group(1)
    info_start += res.end(1)
    filename.append(formatFileName(temptxt))
  return filename

def getFileCode(txt):
  class CodeHTMLParser(HTMLParser):
    inContainerDiv = False
    inFieldSet = False
    inPre = False
    inTextarea = False
    Code = []
    isRunning = True
    countDiv = 0
    nowData = ''

    def handle_starttag(self, tag, attrs):
      if self.isRunning == False: return None
      if tag == 'div':
        if self.inContainerDiv == True:
          self.countDiv = self.countDiv + 1
        for i in attrs:
          if i[0] == 'class':
            if i[1] == 'field-container':
              self.inContainerDiv = True
      if tag == 'fieldset':
        self.inFieldSet = True
      if tag == 'pre':
        self.inPre = True
      if tag == 'textarea':
        self.inTextarea = True
    def handle_endtag(self, tag):
      if self.isRunning == False: return None
      if self.inContainerDiv == True:
        if (self.countDiv - 1 < 0):
          isRunning = False
        else:
          self.countDiv = self.countDiv - 1

      if tag == 'fieldset':
        self.inFieldSet = False
      if tag == 'pre':
        self.Code.append(self.nowData)
        self.nowData = ''
        self.inPre = False
      if tag == 'textarea':
        self.Code.append(self.nowData)
        self.nowData = ''
        self.inTextarea = False
    def handle_data(self, data):
      if self.isRunning == False: return None
      if self.inPre:
        # self.Code.append(data)
        self.nowData += data
      if self.inTextarea:
        # self.Code.append(data)
        self.nowData += data

  parser = CodeHTMLParser()
  parser.feed(txt)
  return parser.Code


cj = cookielib.CookieJar();

username = raw_input("Please input your username: ")
password = raw_input("Please input your password: ")
ass_id   = raw_input("Please input the assignment id: ")
path     = raw_input("Please input the path you want to save in: ")


hosturl = 'http://eden.sysu.edu.cn/m/login/?next=/m/ass/' + ass_id + '/'
posturl = 'http://eden.sysu.edu.cn/'

cookie_headers = {
  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
  'Accept-Encoding':'gzip, deflate, sdch',
  'Accept-Language':'zh-CN,zh;q=0.8',
  'Cache-Control':'max-age=0',
  'Connection':'keep-alive',
  'Host':'eden.sysu.edu.cn',
  'Upgrade-Insecure-Requests':1,
  'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
}

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj));
urllib2.install_opener(opener);
request = urllib2.Request(hosturl, None, cookie_headers)
response = urllib2.urlopen(request);
# print response.info()
token = ''
sessionid = ''
# get the first csrftoken
for i in cj:
  if i.name == 'csrftoken':
    token = i.value
  elif i.name == 'sessionid':
    sessionid = i.value

# prepare for the next request

# postform
postdata = {
  'csrfmiddlewaretoken': token,
  'username': username,
  'password': password,
  'next':'/m/ass/' + ass_id + '/'
}
postdata = urllib.urlencode(postdata)
print postdata

# headers when second request
headers = {
  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
  'Accept-Encoding':'gzip, deflate',
  'Accept-Language':'zh-CN,zh;q=0.8',
  'Cache-Control':'max-age=0',
  'Connection':'keep-alive',
  'Content-Length':114,
  'Content-Type':'application/x-www-form-urlencoded',
  'Cookie':'csrftoken=' + token,
  'Host':'eden.sysu.edu.cn',
  'Origin':'http://eden.sysu.edu.cn',
  'Referer':'http://eden.sysu.edu.cn/m/login/?next=/m/ass/6183/',
  'Upgrade-Insecure-Requests':1,
  'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
}

request = urllib2.Request('http://eden.sysu.edu.cn/m/login/?next=/m/ass/' + ass_id + '/', postdata, headers)

# request. Now in ?next=/m/ass/$ass_id/
response = urllib2.urlopen(request)
# get the cookie
for i in cj:
  if i.name == 'csrftoken':
    token = i.value
  if i.name == 'sessionid':
    sessionid = i.value


# print response.info()
# print 'I think my login success...'


# now request to m/ass/$ass_id/
headers = {
  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
  'Accept-Encoding':'gzip, deflate, sdch',
  'Accept-Language':'zh-CN,zh;q=0.8',
  'Cache-Control':'max-age=0',
  'Connection':'keep-alive',
  'Cookie':'csrftoken=' + token + '; sessionid=' + sessionid,
  'Host':'eden.sysu.edu.cn',
  'Referer':'http://eden.sysu.edu.cn/m/login/?next=/m/ass/' + ass_id + '/',
  'Upgrade-Insecure-Requests':1,
  'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
}

# print headers
request = urllib2.Request('http://eden.sysu.edu.cn/m/ass/' + ass_id + '/', None, headers)
response = urllib2.urlopen(request)

# print response.info()
text = response.read()

filename = getFileName(text)
filecode = getFileCode(text)
count = 0
name_len = len(filename)
for (i,j) in zip(filecode, filename):
  if count < name_len:
    f = open(j, 'w+')
    f.write(i)
    f.close()
    # print filename[count]
    # print i
    print j
    count = count + 1
print count
print 'Success'
