#!/usr/bin/python3
import sys
import time
import os
import zipfile
import threading
import Config
from DirOrFileToOSS import DirOrFileToOSS


def runCmd(cmd):
    print(cmd)
    result = os.popen(cmd)
    res = result.read()
    str = ''
    for line in res.splitlines():
        print(line)
        str = str + line
    return str


if __name__ == "__main__":
    BACKUP_DIR = Config.dnmpDirPath+'/data/gitlab/backups'
    runCmd('rm -rf '+BACKUP_DIR+'/*')
    runCmd('docker exec gitlab gitlab-rake gitlab:backup:create')
    fileName = runCmd('ls '+BACKUP_DIR+' -t | head -n 1')

    print('正在把gitlab上传至oss空间...')
    config = {
        'accessKeyID': Config.accessKeyID,
        'accessKeySecret': Config.accessKeySecret,
        'endpoint': Config.endpoint,
        'bucketName': Config.bucketName,
        'baklist': [
            # git备份
            {
                # 要备份的目录(后面不带/)或文件全路径
                'path': BACKUP_DIR+'/'+fileName,
                # 本地备份路径
                'locBakPath': Config.bakRootPath + '/gitlabbak',
                # oss上传路径,结尾带 /
                'ossPath': 'DataAutoBak/gitlabbak/',
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
