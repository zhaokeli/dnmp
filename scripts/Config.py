#! python3
import os
import platform
bakRootPath = os.path.abspath('..') + '/data/databak'
# oss配置
accessKeyID = 'LTAI**********MeT'
accessKeySecret = 'aOLFLan********N4VAuXA1sKGKB'
endpoint = 'oss-cn-beijing.aliyuncs.com'
bucketName = 'xia***********e'

logPath = os.path.abspath('..') + '/logs/bak'
# 数据库sql备份,请确保mysqldump在环境变量中能执行,也可以直接在下面设置
mysqldump_path = ''
db_host = "127.0.0.1"
db_user = "root"
db_passwd = "******"
db_name = ['mysql', 'ank_stat', 'ank_blog']
db_charset = "utf8"
isDocker = True
if platform.system() == 'Windows':
    isDocker = False
