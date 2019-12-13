#! python3
from DirOrFileToOSS import DirOrFileToOSS

config = {
    # oss配置信息
    'accessKeyID': 'LTAIyRFV9OAyiMeT',
    'accessKeySecret': 'aOLFLanFp0YQDKZeJN4VAuXA1sKGKB',
    'endpoint': 'oss-cn-beijing.aliyuncs.com',
    'bucketName': 'xiangce-archive',
    # 'ossBakPath': 'DataAutoBak/',  # 远程oss备份路径
    # 'locBakpath': 'D:/gitbak',  # 本地备份路径
    'baklist': [
        {
            # 要备份的目录(后面不带/)或文件全路径
            'path': 'E:/yy',
            # 本地备份路径
            'locBakPath': 'D:/gitbak',
            # oss上传路径
            'ossPath': 'DataAutoBak/',
            # 要忽略的文件或目录
            'ignoreDirOrFile': ['.git', 'runtime', 'Data', 'aspnet_client', 'imagethumb'],
            # 是否删除本地备份,如果上传oss为False时此设置不会生效
            'isRemoveLocBak': False,
            # 是否上传oss
            'isUploadOss':True

        }]
}
if __name__ == '__main__':
    bak = DirOrFileToOSS(config)
    bak.run()
