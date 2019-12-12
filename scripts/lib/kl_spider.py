import sys
import re
import random
import os
import threading
import time
import _thread
import kl_http
import kl_db
import kl_reg
import kl_progressbar
import kl_log
from kl_print import *
from urllib.parse import urlparse

log = kl_log.kl_log('spider')
regex = kl_reg
http = kl_http.kl_http()
# mylock = _thread.allocate_lock()#线程锁
# self.mylock.acquire() #Get the lock
# self.mylock.release()  #Release the lock.
http.setproxy('', '', '127.0.0.1:8087')
db = kl_db.mysql({
    'host': 'localhost',
            'user': 'root',
            'passwd': 'adminrootkl',
            'db': 'bokedaquan',
            'prefix': 'kl_',
            'charset': 'utf8'
})
proxypath = '../tool/proxy/proxy.txt'
proxylist = []
if os.path.exists(proxypath):
    f = open(proxypath, 'r')
    s = f.read()
    f.close()
    proxylist = s.splitlines()


class urlspider(object):
    """docstring for urlspider"""

    def __init__(self, arg):
        super(urlspider, self).__init__()
        self.isproxy = False
        self.arg = arg
        self.hostname = arg['hostname']
        self.linkreg = '<a[^><\n]*?href=["|\']{0,1}([^><\n]*?(?:00_00)[^><\n]*?)["|\']{0,1}[^><\n]*?>.*?</a>'
        self.url = arg['url']
        self.charset = arg['charset']
        self.mb_url_reg = arg['mb_url_reg']
        self.mb_con_reg = arg['mb_con_reg']
        self.link_tezheng = arg['link_tezheng']
        self.shendu = int(arg['shendu'])
        self.url_table = arg['name'] + '_url'
        self.content_table = arg['name'] + '_content'
        self.urled_table = arg['name'] + '_urled'
        self.content_sql = arg['content_sql']
        self.con_field = arg['field']
        self.maxthread = 4
        self.threadnum = 0
        self.progress = kl_progressbar.kl_progressbar('正在运行中')
        self.mylock = _thread.allocate_lock()  # 线程锁
        self.init()

    # 创建数据表
    def init(self):
        # 创建已经采集的url数据表
        sql = '''\
CREATE TABLE `[TABLE]` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(255) DEFAULT NULL,
  `status` smallint(3) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=77089 DEFAULT CHARSET=utf8;'''
        sql = sql.replace('[TABLE]', db.prefix + self.urled_table)
        db.query(sql)
        # 创建url数据表
        sql = '''\
CREATE TABLE `[TABLE]` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(255) DEFAULT NULL,
  `src_url` varchar(255) DEFAULT NULL,
  `hostname` varchar(255) DEFAULT NULL,
  `update_time` int(11) DEFAULT NULL,
  `status` smallint(3) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=77089 DEFAULT CHARSET=utf8;'''
        sql = sql.replace('[TABLE]', db.prefix + self.url_table)
        db.query(sql)
        # 创建content内容数据表
        sql = '''\
CREATE TABLE `[TABLE]` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
    [CONTENT_SQL]
  `src_url` varchar(255) DEFAULT NULL,
  `update_time` int(11) DEFAULT NULL,
  `status` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=77089 DEFAULT CHARSET=utf8;'''
        sql = sql.replace('[TABLE]', db.prefix + self.content_table)
        sql = sql.replace('[CONTENT_SQL]', self.content_sql)
        db.query(sql)

        # 创建content内容数据表
        sql = '''\
DROP TABLE IF EXISTS `[TABLE]`;
CREATE TABLE `[TABLE]` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=77089 DEFAULT CHARSET=utf8;'''
        sql = sql.replace('[TABLE]', db.prefix + 'runtimeing')
        db.query(sql)

    def run(self):
        self.shenduurl(self.url)
        self.caijicon()

    # 随机取一个代理
    def get_proxy(self):
        proxylen = len(proxylist)
        if proxylen <= 0:
            print('There is no available proxy server!')
            sys.exit()
        while True:
            pro = proxylist[random.randint(0, proxylen - 1)]
            if pro != "":
                return pro

    def shenduurl(self, url, cur_shendu=1):
        #global  mylock
        url = url.strip()

        # self.mylock.acquire()
        result = db.table(self.urled_table).where({'url': url}).count()
        runing = db.table('runtimeing').where({'url': url}).count()
        if (result > 0 or runing > 0)and not db.lasterror:
            return True

        # 添加正在采集的地址
        db.table('runtimeing').add({'url': url})
        # self.mylock.release()

        ht = kl_http.kl_http()
        ht.autoUserAgent = True
        r = None
        content = ''
        changshi = 1
        while True:
            try:
                print("collection page %s depth:%d  request nums:%d" % (url, cur_shendu, changshi))
                if self.isproxy:
                    daili = self.get_proxy()
                    print_green("using proxy:%s" % daili)
                    ht.setproxy('', '', daili)
                r = ht.geturl(url)
                if ht.lasterror == None:
                    content = r.read().decode(self.charset)
                    break
                else:
                    print_red(ht.lasterror)
                    changshi = changshi + 1
            except Exception as e:
                content = ''
                print_red(e)
                changshi = changshi + 1
            # finally:
            #     del ht
        if content:
            # 查找目标url
            mburl_list = regex.findall(self.mb_url_reg, content, regex.I | regex.S)
            # 去重
            mburl_list = list(set(mburl_list))
            # self.mylock.acquire()
            self.adddata(mburl_list, url)
            # self.mylock.release()
            # 深度查找
            if cur_shendu < self.shendu or self.shendu == 0:
                cur_shendu += 1
                # 查找特征列表
                for x in self.link_tezheng:
                    xiangsereg = self.linkreg.replace('00_00', x)
                    sdurl_list = regex.findall(xiangsereg, content, regex.I | regex.S)
                    # self.mylock.acquire()
                    sdurl_list = self.__filterurl(sdurl_list, url)
                    # self.mylock.release()
                    for j in sdurl_list:
                        # if cur_shendu==2:
                        if False:
                            while True:
                                #print('curthread nums:%d'%self.threadnum)
                                self.progress.show()
                                # 只有第一次进入这个函数时才可以启动线程
                                if self.threadnum < self.maxthread:
                                    self.threadnum += 1
                                    threading.Thread(target=self.shenduurl, args=(self.formaturl(url, j), cur_shendu,)).start()
                                    break
                                time.sleep(1)
                        else:
                            self.shenduurl(self.formaturl(url, j), cur_shendu)

        # 更新已经采集过的网址为采集完成状态
        db.table(self.urled_table).add({'url': url})
        db.table('runtimeing').where({'url': url}).delete()
        self.threadnum -= 1
    # 过滤已经查询过后地址

    def __filterurl(self, urllist, requesturl):
        relist = []
        sdurl_list = list(set(urllist))
        for i in sdurl_list:
            i = i.strip()
            j = self.formaturl(requesturl, i)
            result = db.table(self.urled_table).where({'url': j}).count()
            resing = db.table('runtimeing').where({'url': j}).count()
            if not result and not resing and not db.lasterror:
                relist.append(i)
        return relist
     # 下面开始采集内容

    def caijicon(self):
        while 1:
            try:
                dlist = db.table(self.url_table).limit(10).order('id asc').where({
                    'status': 0
                }).getarr()
                if not dlist:
                    break
                for i in dlist:
                    url = self.formaturl(i['src_url'], i['url'])

                    ht = kl_http.kl_http()
                    ht.autoUserAgent = True
                    r = None
                    content = ''
                    changshi = 1
                    while True:
                        try:
                            print("collection content %s  request nums:%d" % (url, changshi))
                            if self.isproxy:
                                daili = self.get_proxy()
                                print_green("using proxy:%s" % daili)
                                ht.setproxy('', '', daili)
                            r = ht.geturl(url)
                            if ht.lasterror == None:
                                content = r.read().decode(self.charset)
                                break
                            else:
                                # print(ht.lasterror)
                                changshi = changshi + 1
                        except Exception as e:
                            content = ''
                            print_red(e)
                            changshi = changshi + 1
                    if content:
                        # 查找目标url
                        mbcon_list = regex.findall(self.mb_con_reg, content, regex.I | regex.S)
                        adddata = {}
                        for m in mbcon_list:
                            for o, p in self.con_field.items():
                                adddata[o] = m[int(p) - 1]

                            resu = db.table(self.content_table).where(adddata).count()
                            if resu < 1:
                                db.table(self.content_table).add(adddata)
                                print_green('added %s' % adddata)
                        db.table(self.url_table).where({'id': i['id']}).save({'status': r.code})
            except Exception as e:
                print_red(e)

    # 格式化请求的路径
    def formaturl(self, requestpath, curpath):
        # 请求的url目录
        urldir = os.path.dirname(requestpath)
        url = urlparse(requestpath)
        protocol = url[0]
        hostname = url[1]
        if curpath[0:1] == '/':
            return '%s://%s%s' % (protocol, hostname, curpath)
        else:
            return urldir + '/' + curpath
    # 添加数据到数据库

    def adddata(self, urllist, src_url):
        for i in urllist:
            result = db.table(self.url_table).where({
                'hostname': self.hostname,
                'url': i
            }).count()
            if result < 1 and not db.lasterror:
                res = db.table(self.url_table).add({
                    'url': i,
                    'hostname': self.hostname,
                    'status': 0,
                    'update_time': time.time(),
                    'src_url': src_url
                })
                if res <= 0:
                    log.write('add %s error:%s' % (i, db.lasterror))
                    log.write('lastsql:%s' % db.getlastsql())
                else:
                    print("add url：%s" % i)


if __name__ == '__main__':
    # 链接url正则
    cjurl = [
        {
            # 采集项目的名字
            'name': 'boke',
            'hostname': 'http://lusongsong.com',
            # 入口地址
            'url': 'http://lusongsong.com/daohang/',
            # 抓取进入的深度
            'shendu': 2,
            # 类似网址入口正则(精确要进入采集的网址)
            'link_tezheng': ['\/daohang\/webdir\-[^><\n]*?\.html'],
            # 目标网址正则
            'mb_url_reg':'<a[^><\n]*?href=["|\']?([^><\n]*?(?:showurl_\d+?\.html)[^><\n]*?)["|\']?[^><\n]*?>.*?</a>',
            # 目标内容正则(至少要有两个正则分组)
            'mb_con_reg':'点此打开.*?【(.*?)】.*?网址.*?<a.*?href="(.*?)".*?>.*?</a>',
            # 内容正则中的分组对应的字段信息
            'field':{
                'title': 1,
                'url': 2
            },
            # 采集到的内容字段sql语句
            'content_sql': '''\
                  `title` varchar(255) DEFAULT NULL,
                  `url` varchar(255) DEFAULT NULL,
                  `descr` varchar(255) DEFAULT NULL,
                  `area` varchar(255) DEFAULT NULL,
                  `blog_type` varchar(255) DEFAULT NULL,''',
            'charset': 'utf-8',
        }
    ]

    for i in cjurl:
        spi = urlspider(i)
        spi.run()
    input('it is conllected,please press any key to continue...')
