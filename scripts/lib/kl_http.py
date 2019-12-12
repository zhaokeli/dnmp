#-*-coding:UTF-8-*-
'''
+----------------------------------------------------------------------
// | Author: 赵克立 <735579768@qq.com> <http://www.zhaokeli.com>
// |http数据库操作类
+----------------------------------------------------------------------
// | 自动保存请求中的cookies,
// | setcookies({})可以自定义cookies
// | setheaders({})自定义请求头信息
// |
// |
'''
import urllib.request
import os
import random
import time
import urllib.parse
import http.cookiejar
import socket
import re
# socket.setdefaulttimeout(60)           #10秒内没有打开web页面，就算超时

# 创建目录


def create_dir(dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
useragent = [
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
]


class kl_http:

    def __init__(self):
        self.lasterror = None
        self.proxy = {
            'username': '',
            'password': '',
            'proxyserver': ''
        }
        self.responsetime = 0
        self.hostname = ''
        self.headers = {}
        self.cookies = {}
        self.opener = None
        self.ckjar = None
        self.autoUserAgent = True
        self.request = None
        self.timeout = 10

    def __del__(self):
        try:
            self.request.close()
        except Exception as e:
            pass
    # 重置会话

    def resetsession(self):
        self.opener = None

    # 设置cookies并创建会话
    def __setcookies(self, url):
        if self.opener != None:
            return None
        urls = urllib.parse.urlsplit(url)
        self.hostname = urls[1]
        if os.path.exists('./data/cookies') == False:
            os.makedirs('./data/cookies')
        # 创建一个带cookie的网络打开器,后面的get post请求都使用这个打开
        self.ckjar = http.cookiejar.MozillaCookieJar("./data/cookies/cookies-%s.txt" % (self.hostname))
        try:
            # 加载已存在的cookie，尝试此cookie是否还有效
            self.ckjar.load(ignore_discard=True, ignore_expires=True)
        except Exception:
            # 加载失败，说明从未登录过，需创建一个cookie kong 文件
            self.ckjar.save(ignore_discard=True, ignore_expires=True)
        self.__addcookies()

        # 代理
        if self.proxy['proxyserver']:
            proxy = 'http://%s:%s@%s' % (self.proxy['username'], self.proxy['password'], self.proxy['proxyserver'])
            proxy_handler = urllib.request.ProxyHandler({'http': proxy})
            ckproc = urllib.request.HTTPCookieProcessor(self.ckjar)
            self.opener = urllib.request.build_opener(ckproc, proxy_handler)
            return None
        elif self.autoUserAgent:
            self.opener = urllib.request.build_opener()
            return None
        else:
            ckproc = urllib.request.HTTPCookieProcessor(self.ckjar)
            self.opener = urllib.request.build_opener(ckproc)
            return None

    # 添加自定义的cookies
    def __addcookies(self):
        for a, b in self.cookies.items():
            cookie_item = http.cookiejar.Cookie(
                version=0, name=a, value=b,
                port=None, port_specified=None,
                domain=self.hostname, domain_specified=None, domain_initial_dot=None,
                path=r'/', path_specified=None,
                secure=None,
                expires=None,
                discard=None,
                comment=None,
                comment_url=None,
                rest=None,
                rfc2109=False,
            )
            self.ckjar.set_cookie(cookie_item)    # Apply each cookie_item to cookiejar

    # 设置代理服务器
    def setproxy(self, username, password, proxyserver):
        self.opener = None
        self.proxy['username'] = username
        self.proxy['password'] = password
        self.proxy['proxyserver'] = proxyserver

    # 设置请求的header头
    def setheaders(self, data):
        if type(data) == type(''):
            data = data.splitlines()
            for i in data:
                if i != "":
                    inde = i.find(':')
                    if inde != -1:
                        self.headers[i[0:inde]] = i[inde + 1:]
        elif type(data) == type({}):
            self.headers = data
        self.resetsession()

    def setcookies(self, data):
        if type(data) == type(''):
            data = data.split(';')
            for i in data:
                if i != '':
                    tem = i.split('=')
                    self.cookies[tem[0]] = tem[1]
        elif type(data) == type({}):
            self.cookies = data
        self.resetsession()

    # 设置超时
    def settimeout(self, timeout=60):
        self.timeout = timeout

    # get取网页数据
    def geturl(self, url, data={}):
        self.lasterror = None
        data = self.__formatpostdata(data)
        global useragent
        self.__setcookies(url)
        self.request = None
        try:
            params = urllib.parse.urlencode(data)  # .encode(encoding='UTF8')
            req = ''
            if params == '':
                req = urllib.request.Request(url)
            else:
                req = urllib.request.Request(url + '?%s' % (params))

            # 设置headers
            for a, b in self.headers.items():
                req.add_header(a, b)
            req.add_header('Referer', url)
            if self.autoUserAgent or self.autoUserAgent:
                usag = random.randint(0, 18)
                req.add_header('User-Agent', useragent[usag])
            starttime = time.time()
            self.request = self.opener.open(req, timeout=self.timeout)
            self.responsetime = time.time() - starttime
            self.ckjar.save(ignore_discard=True, ignore_expires=True)
            return self.request
        except urllib.error.HTTPError as e:
            # print(e.code)
            self.lasterror = e
            return self.request
        except urllib.error.URLError as e:
            # print(e.reason)
            self.lasterror = e
            return self.request
        except Exception as e:
            self.lasterror = e
            return self.request
    # 处理post字符串

    def __formatpostdata(self, data):
        if type(data) == type({}):
            return data
        elif type(data) == type(''):
            data = re.split('\r?\n|&', data)
            temarr = {}
            for i in data:
                inde = i.find(':')
                if inde != -1:
                    temarr[i[0:inde]] = i[inde + 1:]
                inde = i.find('=')
                if inde != -1:
                    temarr[i[0:inde]] = i[inde + 1:]
            return temarr
        else:
            return {}

    # get取网页数据
    def posturl(self, url, data=''):
        self.lasterror = None
        data = self.__formatpostdata(data)
        global useragent
        self.__setcookies(url)
        self.request = None
        try:
            params = urllib.parse.urlencode(data).encode(encoding='UTF8')
            req = urllib.request.Request(url, data=params, headers=self.headers)
            req.add_header('Referer', url)

            if self.autoUserAgent or self.autoUserAgent:
                usag = random.randint(0, 18)
                req.add_header('User-Agent', useragent[usag])
            starttime = time.time()
            self.request = self.opener.open(req, timeout=self.timeout)
            self.responsetime = time.time() - starttime
            self.ckjar.save(ignore_discard=True, ignore_expires=True)
            return self.request
        except urllib.error.HTTPError as e:
            # print(e.code)
            self.lasterror = e
            return self.request
        except urllib.error.URLError as e:
            # print(e.reason)
            self.lasterror = e
            return self.request
        except Exception as e:
            self.lasterror = e
            return self.request

    # 支持断点续传
    def downfile(self, url, outdir='./', outfilename=''):
        if not outfilename:
            outfilename = os.path.basename(url)
            filepath = outdir + '/' + outfilename
            temfilepath = filepath + '.tmp'
        try:
            create_dir(outdir)
            req = urllib.request.Request(url)
            req.add_header('Referer', url)
            # 实现断点下载文件

            # 已经下载的长度
            downloadedlen = 0
            if os.path.exists(temfilepath):
                downloadedlen = os.path.getsize(temfilepath)
            req.add_header('Range', 'bytes=%d-' % (downloadedlen))
            print('start download file...')
            r = self.opener.open(req)

            # 写文件到本地
            binfile = open(temfilepath, "ab")
            try:
                c = downloadedlen
                totallen = r.length
                tlen = r.getheader('Content-Range')
                if tlen:
                    totallen = int(tlen[tlen.find('/') + 1:])
                print('Download size(%d) %s to %s' % (totallen, url, filepath))
                while True:
                    s = r.read(1024 * 10)
                    if len(s) == 0:
                        break
                    binfile.write(s)
                    c += len(s)
                    print('Downloading %0.3f %%' % (100 * c / totallen))
                binfile.close()
                if os.path.exists(filepath):
                    os.unlink(filepath)
                os.rename(temfilepath, filepath)
                return filepath

            except Exception as e:
                print(e)
                binfile.close()
                return None

        except Exception as e:
            # 416请求的开始点不在指定范围，可能是已经下载完啦
            if e.code == 416:
                if os.path.exists(filepath):
                    os.unlink(filepath)
                os.rename(temfilepath, filepath)
                return filepath
            print(e)
            return None

if __name__ == '__main__':
    import chardet
    import io
    import sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')  # 改变标准输出的默认编码
    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')         #改变标准输出的默认编码
    ht = kl_http()
    ht.setheaders('''\
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36
Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2
''')
    # ht.setcookies('ankc_admin__uid__=ainiku%3A%7B%22u%22%3A%22MDAwMDAwMDAwMLyQiNbHupWh%22%2C%22p%22%3A%22MDAwMDAwMDAwMLyQiNbHupbdxGRqlcaUqHU%22%7D;')
    # ht.setproxy('','','127.0.0.1:8087')
    # r=ht.posturl(r'http://127.0.0.1/')
    # r=ht.geturl(r'http://1212.ip138.com/ic.asp')
    r = ht.geturl(r'http://ss.ainiku.com/')
    if r:
        re = r.read()  # .decode('gbk').encode('utf8')
        charset = chardet.detect(re)
        chars = charset['encoding']
        print(chars)
        strr = re.decode(chars)
        print(strr)
    url = 'http://dlsw.baidu.com/sw-search-sp/soft/e7/10520/KanKan_V2.7.8.2126_setup.1416995191.exe'
    outdir = "./downs"
    print(ht.downfile(url, outdir))
    os.system("pause")
