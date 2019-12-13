#! python3
from UploadOSS import UploadOSS

config = {
    # oss配置信息
    'accessKeyID': 'LTAIyRFV9OAyiMeT',
    'accessKeySecret': 'aOLFLanFp0YQDKZeJN4VAuXA1sKGKB',
    'endpoint': 'oss-cn-beijing.aliyuncs.com',
    'bucketName': 'xiangce-archive',
    'ossBakPath': 'DataAutoBak/',  # 远程oss备份路径
    'locBakpath': 'D:/gitbak',  # 本地备份路径
    'baklist': ['E:/yy', 'E:/GitServer/dnmp/scripts/UploadOSS.py'],  # 要备份的目录(后面不带/)或文件全路径
    'ignoreDirOrFile': ['.git', 'runtime', 'Data', 'aspnet_client', 'imagethumb']  # 要忽略的文件或目录
}
if __name__ == '__main__':
    bak = UploadOSS(config)
    bak.run()
