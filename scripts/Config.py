#! python3
import os
bakRootPath = os.getcwd() + '/../data/databak'
# oss配置
accessKeyID = 'LTAIyRFV9OAyiMeT'
accessKeySecret = 'aOLFLanFp0YQDKZeJN4VAuXA1sKGKB'
endpoint = 'oss-cn-beijing.aliyuncs.com'
bucketName = 'xiangce-archive'


# 数据库sql备份,请确保mysqldump在环境变量中能执行,也可以直接在下面设置
mysqldump_path = ''
db_host = "127.0.0.1"
db_user = "root"
db_passwd = "adminrootkl"
db_name = ['ank_stat', 'ank_blog']
db_charset = "utf8"
