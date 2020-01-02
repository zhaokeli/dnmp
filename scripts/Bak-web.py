#!/usr/bin/python3
from DirOrFileToOSS import DirOrFileToOSS
import Config
config = {
    'accessKeyID': Config.accessKeyID,
    'accessKeySecret': Config.accessKeySecret,
    'endpoint': Config.endpoint,
    'bucketName': Config.bucketName,
    'baklist': [
        # web备份
        {
            # 要备份的目录(后面不带/)或文件全路径
            'path': Config.dnmpDirPath + '/www/dflz.org',
            # 本地备份路径
            'locBakPath': Config.bakRootPath + '/dirbak',
            # oss上传路径,结尾带 /
            'ossPath': 'DataAutoBak/webbak/',
            # 要忽略的文件或目录
            'ignoreDirOrFile': ['.vscode', '.git', 'runtime', 'Data', 'aspnet_client', 'imagethumb'],
            # 是否删除本地备份,如果上传oss为False时此设置不会生效
            'isRemoveLocBak': True,
            # 是否上传oss
            'isUploadOss':True

        },
        # {
        #     # 要备份的目录(后面不带/)或文件全路径
        #     'path': Config.dnmpDirPath + '/www',
        #     # 本地备份路径
        #     'locBakPath': Config.bakRootPath + '/dirbak',
        #     # oss上传路径,结尾带 /
        #     'ossPath': 'DataAutoBak/webbak/',
        #     # 要忽略的文件或目录
        #     'ignoreDirOrFile': ['.vscode', '.git', 'runtime', 'Data', 'aspnet_client', 'imagethumb'],
        #     # 是否删除本地备份,如果上传oss为False时此设置不会生效
        #     'isRemoveLocBak': False,
        #     # 是否上传oss
        #     'isUploadOss':True

        # },
    ]
}
if __name__ == '__main__':
    bak = DirOrFileToOSS(config)
    bak.run()
