# -*- coding: UTF-8 -*-
import sys
import time
import io
import os
import time
import zipfile
import threading
import oss2
import Config
from DirOrFileToOSS import DirOrFileToOSS
isDelFile = True
db_host = Config.db_host
db_user = Config.db_user
db_passwd = Config.db_passwd
db_name = Config.db_name
db_charset = Config.db_charset
mysqldump_path = Config.mysqldump_path
# 当前目录日期后缀
dirsubfix = time.strftime('%Y/%m', time.localtime())
locBakPath = Config.bakRootPath + '/sqlbak/' + dirsubfix
if mysqldump_path == '':
    mysqldump_path = 'mysqldump'
isDocker = Config.isDocker


class kl_log:

    def __init__(self, filename='kl_log'):
        self.filename = filename + '-'
        self.filepath = Config.logPath + '/'

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


def runCmd(str):
    print(str)
    os.system(str)


def bakmysql(db_name, sss):
    try:
        global baknum
        baknum = baknum + 1
        db_backup_name = locBakPath + r"/%s_%s.sql" % (time.strftime("%Y-%m-%d_%H-%M-%S"), db_name)
        if os.path.exists(os.path.dirname(db_backup_name)) == False:
            os.makedirs(os.path.dirname(db_backup_name))
        zip_src = db_backup_name
        zip_dest = zip_src + ".zip"
        database.append(zip_dest)

        print("开始备份数据库:%s..." % db_name)
        if isDocker:
            runCmd("docker exec -it mysql mysqldump --skip-comments -u%s -p%s %s  --default_character-set=%s > %s" % (db_user, db_passwd, db_name, db_charset, db_backup_name))
        else:
            runCmd(mysqldump_path + " --skip-comments -h%s -u%s -p%s %s  --default_character-set=%s    > %s" % (db_host, db_user, db_passwd, db_name, db_charset, db_backup_name))
        if os.path.isfile(db_backup_name):
            print("开始压缩数据库:%s..." % db_name)
            f = zipfile.ZipFile(zip_dest, 'w', zipfile.ZIP_DEFLATED)
            [dirname, filename] = os.path.split(zip_src)
            f.write(zip_src, './' + filename)
            f.close()
            os.remove(zip_src)
            print("数据库%s备份完成!" % db_name)
        else:
            print("数据库SQL文件不存在!")
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
    db_backup_name = locBakPath + r"/database-%s.zip" % (time.strftime("%Y-%m-%d_%H-%M-%S"))
    f = zipfile.ZipFile(db_backup_name, 'w', zipfile.ZIP_DEFLATED)
    for i in database:
        if os.path.isfile(i):
            [dirname, filename] = os.path.split(i)
            f.write(i, './' + filename)
            os.remove(i)
    f.close()

    print('正在把数据库上传至oss空间...')
    config = {
        'accessKeyID': Config.accessKeyID,
        'accessKeySecret': Config.accessKeySecret,
        'endpoint': Config.endpoint,
        'bucketName': Config.bucketName,
        'baklist': [
            # git备份
            {
                # 要备份的目录(后面不带/)或文件全路径
                'path': db_backup_name,
                # 本地备份路径
                'locBakPath': Config.bakRootPath + '/sqlbak',
                # oss上传路径,结尾带 /
                'ossPath': 'DataAutoBak/sqlbak/',
                # 要忽略的文件或目录
                'ignoreDirOrFile': ['.git', 'runtime', 'Data', 'aspnet_client', 'imagethumb'],
                # 是否删除本地备份,如果上传oss为False时此设置不会生效
                'isRemoveLocBak': False,
                # 是否上传oss
                'isUploadOss':True

            },
        ]
    }
    bak = DirOrFileToOSS(config)
    bak.run()
