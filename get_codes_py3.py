import urllib.request, urllib.error, urllib.parse
import http.cookiejar
import re
import os
from html.parser import HTMLParser

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
      if self.inContainerDiv:
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
      if self.inContainerDiv:
        if self.inPre or self.inTextarea:
          self.nowData += data
    def handle_entityref(self, data):
      if self.inContainerDiv:
        if self.inPre or self.inTextarea:
          if data == 'nbsp':
            self.nowData += ' '
          elif data == 'lt':
            self.nowData += '<'
          elif data == 'gt':
            self.nowData += '>'
          elif data == 'amp':
            self.nowData += '&'
          elif data == 'quot':
            self.nowData += '"'
          elif data == '#39':
            self.nowData += "'"

  parser = CodeHTMLParser()
  parser.feed(txt)
  return parser.Code


cj = http.cookiejar.CookieJar();
username = ''
password = ''


config_file = None
config_exist = False
configs = []
if os.path.exists(".eden_config"):
  config_exist = True
  config_file = open(".eden_config","r+")
  for line in config_file:
    configs.append(line)
else:
  config_exist = False

if not config_exist:
  username = input("Please input your username: ")
  password = input("Please input your password: ")
  yes_or_no = input("Do you want to save your username and password, after which you can skip the input(y/n): ")
  err = True
  if yes_or_no.lower() == 'y' or yes_or_no.lower() == 'n':
    err = False
    if yes_or_no.lower() == 'y':
      config_file = open(".eden_config", "w+")
      config_file.write(username + '\n' + password)

  while err:
    yes_or_no = input("Please input y/n")
    if yes_or_no.lower() == 'y' or yes_or_no.lower() == 'n':
      err = False
      if yes_or_no.lower() == 'y':
        config_file = open(".eden_config", "w+")
        config_file.write(username + '\n' + password)
else:
  username = configs[0].replace('\n', '')
  password = configs[1].replace('\n', '')
  print(username)
  print(password)

ass_id   = input("Please input the assignment id: ")
folder_name = input("Please input folder's name you want: ")

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

opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj));
urllib.request.install_opener(opener);
request = urllib.request.Request(hosturl, None, cookie_headers)
response = urllib.request.urlopen(request);

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
postdata = urllib.parse.urlencode(postdata)

# headers when second request
headers = {
  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
  'Accept-Encoding':'gzip, deflate',
  'Accept-Language':'zh-CN,zh;q=0.8',
  'Cache-Control':'max-age=0',
  'Connection':'keep-alive',
  'Content-Type':'application/x-www-form-urlencoded',
  'Cookie':'csrftoken=' + token,
  'Host':'eden.sysu.edu.cn',
  'Origin':'http://eden.sysu.edu.cn',
  'Referer':'http://eden.sysu.edu.cn/m/login/?next=/m/ass/6183/',
  'Upgrade-Insecure-Requests':1,
  'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
}

request = urllib.request.Request('http://eden.sysu.edu.cn/m/login/?next=/m/ass/' + ass_id + '/', postdata.encode('u8'), headers)

# request. Now in ?next=/m/ass/$ass_id/
response = urllib.request.urlopen(request)
# get the cookie
for i in cj:
  if i.name == 'csrftoken':
    token = i.value
  if i.name == 'sessionid':
    sessionid = i.value


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

request = urllib.request.Request('http://eden.sysu.edu.cn/m/ass/' + ass_id + '/', None, headers)
response = urllib.request.urlopen(request)

text = response.read().decode('u8')

filename = getFileName(text)
filecode = getFileCode(text)
count = 0
name_len = len(filename)
if folder_name:
  if os.path.exists(folder_name):
    print('folder exists')
  else:
    os.mkdir(folder_name)
for (i,j) in zip(filecode, filename):
  if count < name_len:
    f = None
    if folder_name:
      f = open(folder_name + '/' + j, 'w+')
    else:
      f = open(j, 'w+')
    f.write(i)
    f.close()
    print(j + ' finished')
    count = count + 1
print(str(count) + ' file(s) copied')
print('Success!')

if config_file:
  config_file.close()