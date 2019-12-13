# -*- coding: UTF-8 -*-
import sys
import time
import io
import os
import time
import zipfile
import threading
import oss2

isDelFile = True
db_host = "127.0.0.1"
db_user = "root"
db_passwd = "adminrootkl"
db_name = ['hmcrm']
db_charset = "utf8"


class kl_log:

    def __init__(self, filename='kl_log'):
        self.filename = filename + '-'
        self.filepath = './data/log/'

    def setpath(self, filepath):
        self.filepath = filepath

    def setfilename(self, filename):
        self.filename = filename + '-'

    def write(self, data='', model='a'):
        fname = time.strftime('%Y-%m-%d', time.localtime())
        fpath = '%s%s%s.log' % (self.filepath, self.filename, fname)
        if os.path.exists(os.path.dirname(fpath)) == False:
            os.makedirs(os.path.dirname(fpath))

        ti = time.strftime('%Y-%m-%d %X', time.localtime())
        f = open(fpath, model)
        f.write("%s: %s\n" % (ti, data))
        f.close()
        return True


log = kl_log()


def bakmysql(db_name, sss):
    try:
        global baknum
        baknum = baknum + 1
        db_backup_name = os.path.split(os.path.realpath(__file__))[0] + r"\data\bakmysql\%s_%s.sql" % (time.strftime("%Y-%m-%d_%H-%M-%S"), db_name)
        if os.path.exists(os.path.dirname(db_backup_name)) == False:
            os.makedirs(os.path.dirname(db_backup_name))
        zip_src = db_backup_name
        zip_dest = zip_src + ".zip"
        database.append(zip_dest)

        print("开始备份数据库:%s..." % db_name)
        os.system("mysqldump --skip-comments -h%s -u%s -p%s %s  --default_character-set=%s    > %s" % (db_host, db_user, db_passwd, db_name, db_charset, db_backup_name))
        print("开始压缩数据库:%s..." % db_name)
        # zip_files(zip_src,zip_dest)
        f = zipfile.ZipFile(zip_dest, 'w', zipfile.ZIP_DEFLATED)
        [dirname, filename] = os.path.split(zip_src)
        f.write(zip_src, './' + filename)
        f.close()
        os.remove(zip_src)
        print("数据库%s备份完成!" % db_name)
        baknum = baknum - 1
    except:
        baknum = baknum - 1
        log.write('备份数据库%s时出错' % db_name, 'bakmysql')


if __name__ == "__main__":
    baknum = 0
    database = []
    for i in db_name:
        time.sleep(1)
        threading.Thread(target=bakmysql, args=(i, '')).start()
    time.sleep(3)
    while baknum != 0:
        time.sleep(1)
        sys.stdout.write('%s个进程备份中...\r' % baknum)
        sys.stdout.flush()
        pass
    # 压缩所有已经备份好的数据库
    print('正在压缩所有数据库为一个文件...')
    db_backup_name = os.path.split(os.path.realpath(__file__))[0] + r"\data\bakmysql\%s_all.zip" % (time.strftime("%Y-%m-%d_%H-%M-%S"))
    f = zipfile.ZipFile(db_backup_name, 'w', zipfile.ZIP_DEFLATED)
    for i in database:
        [dirname, filename] = os.path.split(i)
        f.write(i, './' + filename)
        os.remove(i)
    f.close()

    print('正在把数据库上传至oss空间...')
    # uploadoss(db_backup_name, 'webbak/')
    # if isDelFile:
    #     os.remove(db_backup_name)
