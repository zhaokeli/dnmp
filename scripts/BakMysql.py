#! python3
import sys
sys.path.append('./lib/')
import os
import io
import kl_log
import time
import kl_smtp
import zipfile
import threading
import shutil
import oss2
import config
try:
    # 如果运行环境是gbk
    if sys.stdout.encoding == 'cp936':
        # 改变标准输出的默认编码
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
except:
    pass
# 备份的邮箱
mailto_list = ["735579768@qq.com"]
# 要备份的数据库列表
db_name = ['zhaokeli_com_db_new', 'beian', 'dflz.org', 'ruzhouba.com']
# 数据库目录
mysqldatapath = 'D:/Program Files/Huweishen.com/PHPWEB/MySQL Server 5.6/data/'
# 备份目录
mysqldatabakpath = os.getcwd() + '/databak/'
if not os.path.isdir(mysqldatabakpath):
    os.makedirs(mysqldatabakpath)
# 邮件服务器
mysmtp = kl_smtp.kl_smtp('zhaokeli.com', 'service', 'adminrootkl', 'zhaokeli.com')
# mysmtp=kl_smtp.kl_smtp('163.com','deariloveyoutoever','01227328','smtp.163.com')
log = kl_log.kl_log()
copyFileCounts = 0


def uploadoss(localfile):
    print("start uploadoss...")
    auth = oss2.Auth('LTAIyRFV9OAyiMeT', 'aOLFLanFp0YQDKZeJN4VAuXA1sKGKB')
    endpoint = 'oss-cn-beijing.aliyuncs.com'  # 假设Bucket处于杭州区域
    bucket = oss2.Bucket(auth, endpoint, 'xiangce-archive', enable_crc=False)
    # auth = oss2.Auth('LTAIyRFV9OAyiMeT', 'aOLFLanFp0YQDKZeJN4VAuXA1sKGKB')
    # endpoint = 'oss-cn-shanghai.aliyuncs.com' # 假设Bucket处于杭州区域
    # bucket = oss2.Bucket(auth, endpoint, 'ainiku', enable_crc=False)

    osspath = "databak/%s" % (os.path.basename(localfile))
    print("uploading to %s" % (osspath))
    with open(localfile, 'rb') as fileobj:
        bucket.put_object(osspath, fileobj)
    print("uploadoss success!")


def copyFiles(sourceDir, targetDir):
    global copyFileCounts
    print(sourceDir)
    print(u"%s 当前处理文件夹%s已处理%s 个文件" % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), sourceDir, copyFileCounts))
    for f in os.listdir(sourceDir):
        sourceF = os.path.join(sourceDir, f)
        targetF = os.path.join(targetDir, f)
        if os.path.isfile(sourceF):
            # 创建目录
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            copyFileCounts += 1
            # 文件不存在，或者存在但是大小不同，覆盖
            if not os.path.exists(targetF) or (os.path.exists(targetF) and (os.path.getsize(targetF) != os.path.getsize(sourceF))):
                # 2进制文件
                open(targetF, "wb").write(open(sourceF, "rb").read())
                print(u"%s %s 复制完毕" % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), targetF))
            else:
                print(u"%s %s 已存在，不重复复制" % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), targetF))

        if os.path.isdir(sourceF):
            copyFiles(sourceF, targetF)
# 递归目录


def dfs_get_zip_file(input_path, result):
    files = os.listdir(input_path)
    for file in files:
        if os.path.isdir(input_path + '/' + file):
            dfs_get_zip_file(input_path + '/' + file, result)
        else:
            result.append(input_path + '/' + file)
# 输入路径   输出路径   输出文件名


def zip_path(input_path, output_path, output_name):
    if not os.path.isdir(output_path):
        os.makedirs(output_path)
    f = zipfile.ZipFile(output_path + '/' + output_name, 'w', zipfile.ZIP_DEFLATED)
    filelists = []
    dfs_get_zip_file(input_path, filelists)
    for file in filelists:
        file = file.replace('\\', '/')
        input_path = input_path.replace('\\', '/')
        f.write(file, file.replace(input_path, ''))
    f.close()
    return output_path + r"/" + output_name


def bakmysql(db_name, sss):
    try:
        global baknum
        global mysmtp
        global database_zip
        global mysqldatapath
        global mysqldatabakpath
        baknum = baknum + 1
        db_backup_name = r"%s_%s.zip" % (time.strftime("%Y-%m-%d_%H-%M-%S"), db_name)
        database_zip.append(db_backup_name)

        h_db_name = db_name.replace('.', '@002e')
        if not os.path.exists(mysqldatapath + h_db_name):
            baknum = baknum - 1
            return
        print("copy %s to %s" % (mysqldatapath + h_db_name, mysqldatabakpath + db_name))
        copyFiles(mysqldatapath + h_db_name, mysqldatabakpath + db_name)
        zip_path(mysqldatabakpath + db_name, mysqldatabakpath, db_backup_name)
        shutil.rmtree(mysqldatabakpath + db_name)
        zip_dest = mysqldatabakpath + db_backup_name
        print("数据库%s备份完成!" % db_name)
        zipsize = os.path.getsize(zip_dest)
        if zipsize < 50 * 1024 * 1024:
            print('开始发送邮件...')
            if mysmtp.send_mail(mailto_list, db_name + "数据库备份完成", db_name + "数据库备份完成", zip_dest):
                print("发送成功")
            else:
                print("发送失败")
        else:
            print('数据库%s大于(%s)50M不能发送' % (db_name, zipsize))
        baknum = baknum - 1
    except:
        baknum = baknum - 1
        log.write('备份数据库%s时出错' % db_name, 'bakmysql')

if __name__ == "__main__":
    # 备份线程数
    baknum = 0
    database_zip = []
    for i in db_name:
        time.sleep(1)
        threading.Thread(target=bakmysql, args=(i, '')).start()
    time.sleep(3)
    while baknum > 0:
        time.sleep(1)
        sys.stdout.write('%s个进程备份中...\r' % baknum)
        sys.stdout.flush()
        pass
    # 压缩所有已经备份好的数据库
    print('正在压缩所有数据库为一个文件...')
    db_backup_name = mysqldatabakpath + r"bakmysql_%s_all.zip" % (time.strftime("%Y-%m-%d_%H-%M-%S"))
    f = zipfile.ZipFile(db_backup_name, 'w', zipfile.ZIP_DEFLATED)
    for i in database_zip:
        if not os.path.exists(mysqldatabakpath + i):
            continue
        f.write(mysqldatabakpath + i, i)
        os.remove(mysqldatabakpath + i)
    f.close()
    print('正在把数据库上传至oss空间...')
    uploadoss(db_backup_name)
