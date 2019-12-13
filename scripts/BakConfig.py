#! python3


# oss配置
ossAccessKeyID = 'LTAIyRFV9OAyiMeT'
ossAccessKeySecret = 'aOLFLanFp0YQDKZeJN4VAuXA1sKGKB'
ossEndpoint = 'oss-cn-beijing.aliyuncs.com'
ossBucketName = 'xiangce-archive'


# isRemoveBak = True  # 是否删除本地备份,如果上传oss开启后此项生效
# isUploadOss = True  # 是否备份到oss


# 目录备份
ossBakPath = 'webbak/'  # 远程oss备份路径
bakpath = 'D:/webbak'  # 本地备份路径
# 要备份的目录路径
baklist = ['D:/Program Files/Huweishen.com/PHPWEB/MySQL Server 5.6/data', 'D:/gitweb/zhaokeli.com', 'D:/gitweb/dflz.org']
# 要忽略的文件或目录
ignoreDirOrFile = ['.git', 'runtime', 'Data', 'aspnet_client', 'imagethumb']


# 数据库sql备份
# 备份的邮箱
mailto_list = ["735579768@qq.com"]
# 要备份的数据库列表
db_name = ['zhaokeli_com_db_new', 'beian', 'dflz.org', 'ruzhouba.com']
# 数据库目录
mysqldatapath = 'D:/Program Files/Huweishen.com/PHPWEB/MySQL Server 5.6/data/'
# 备份目录
mysqldatabakpath = '/databak/'
