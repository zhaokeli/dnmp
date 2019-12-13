#! python3
from DirOrFileToOSS import DirOrFileToOSS
import Config
config = {
    'accessKeyID': Config.accessKeyID,
    'accessKeySecret': Config.accessKeySecret,
    'endpoint': Config.endpoint,
    'bucketName': Config.bucketName,
    'baklist': [
        # git备份
        {
            # 要备份的目录(后面不带/)或文件全路径
            'path': 'E:/yy',
            # 本地备份路径
            'locBakPath': Config.bakRootPath + '/gitbak',
            # oss上传路径,结尾带 /
            'ossPath': 'DataAutoBak/gitbak/',
            # 要忽略的文件或目录
            'ignoreDirOrFile': ['.git', 'runtime', 'Data', 'aspnet_client', 'imagethumb'],
            # 是否删除本地备份,如果上传oss为False时此设置不会生效
            'isRemoveLocBak': False,
            # 是否上传oss
            'isUploadOss':True

        },
        # web备份
        {
            # 要备份的目录(后面不带/)或文件全路径
            'path': 'E:/GitServer/zhaokeli.com',
            # 本地备份路径
            'locBakPath': Config.bakRootPath + '/webbak',
            # oss上传路径,结尾带 /
            'ossPath': 'DataAutoBak/webbak/',
            # 要忽略的文件或目录
            'ignoreDirOrFile': ['.vscode', '.git', 'runtime', 'Data', 'aspnet_client', 'imagethumb'],
            # 是否删除本地备份,如果上传oss为False时此设置不会生效
            'isRemoveLocBak': False,
            # 是否上传oss
            'isUploadOss':True

        },
    ]
}
if __name__ == '__main__':
    bak = DirOrFileToOSS(config)
    bak.run()
