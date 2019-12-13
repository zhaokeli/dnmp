#! python3
import os
bakRootPath = os.getcwd() + '/../data/databak'
# oss配置
accessKeyID = 'LTAIyRFV9OAyiMeT'
accessKeySecret = 'aOLFLanFp0YQDKZeJN4VAuXA1sKGKB'
endpoint = 'oss-cn-beijing.aliyuncs.com'
bucketName = 'xiangce-archive'


# 目录备份
ossBakPath = 'webbak/'  # 远程oss备份路径
bakpath = 'D:/webbak'  # 本地备份路径
# 要备份的目录路径
baklist = ['D:/Program Files/Huweishen.com/PHPWEB/MySQL Server 5.6/data', 'D:/gitweb/zhaokeli.com', 'D:/gitweb/dflz.org']
# 要忽略的文件或目录
ignoreDirOrFile = ['.git', 'runtime', 'Data', 'aspnet_client', 'imagethumb']


# 数据库sql备份,请确保mysqldump在环境变量中能执行,也可以直接在下面设置
mysqldump_path = ''
db_host = "127.0.0.1"
db_user = "root"
db_passwd = "adminrootkl"
db_name = ['hmcrm']
db_charset = "utf8"
