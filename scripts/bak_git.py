#! python3
import zipfile
import os
import oss2
import time
import sys
import config
# 是否删除本地备份,如果上传oss开启后此项生效
isRemoveBak = True
# 是否备份到oss
isUploadOss = True
# oss配置信息
AccessKeyID = 'LTAIyRFV9OAyiMeT'
AccessKeySecret = 'aOLFLanFp0YQDKZeJN4VAuXA1sKGKB'
endpoint = 'oss-cn-beijing.aliyuncs.com'
bucketName = 'xiangce-archive'
ossBakPath = 'gitbak/'  # 远程oss备份路径
bakpath = 'D:/gitbak'  # 本地备份路径
# 要备份的目录路径
baklist = ['D:/.scm']
# 要忽略的文件或目录
ignoreDirOrFile = []


def percentage(consumed_bytes, total_bytes):
    if total_bytes:
        sys.stdout.write('{0:.2f}%  {1:.2f}/{2:.2f}M\r'.format(100 * (consumed_bytes / total_bytes),
                                                               consumed_bytes / 1000000, total_bytes / 1000000))
        sys.stdout.flush()


def uploadoss(localfile, remotePath):
    if not os.path.exists(localfile):
        print('localfile is not exists!')
        return
    try:
        print("start uploadoss...")
        auth = oss2.Auth(AccessKeyID, AccessKeySecret)
        bucket = oss2.Bucket(auth, endpoint, bucketName, enable_crc=False)
        osspath = remotePath + os.path.basename(localfile)
        print("uploading to %s" % (osspath))
        with open(localfile, 'rb') as fileobj:
            bucket.put_object(osspath, fileobj, progress_callback=percentage)
        print('\nuploadoss success!')
    except Exception as e:
        print(e)


# 递归目录
def dfs_get_zip_file(input_path, result, ignore=[['.git']]):
    files = os.listdir(input_path)
    for file in files:
        filePath = input_path + '/' + file
        if file in ignore:
            print("ignored: " + filePath)
            continue
        if os.path.isdir(filePath):
            dfs_get_zip_file(filePath, result, ignore)
        else:
            print("added: " + filePath)
            result.append(filePath)


def zip_path(input_path, output_path, ignore=['.git']):
    outdir = os.path.dirname(output_path)
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    f = zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED)
    filelists = []
    dfs_get_zip_file(input_path, filelists, ignore)
    print('start compress file...')
    for file in filelists:
        print('compress: ' + file)
        file = file.replace('\\', '/')
        input_path = input_path.replace('\\', '/')
        f.write(file, file.replace(input_path, ''))
    f.close()
    print('compress complete!')
    return output_path


if __name__ == '__main__':

    for item in baklist:
        dirpath = item
        zippath = "%s/%s-%s.zip" % (bakpath, os.path.basename(item),
                                    time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime()))
        zip_path(dirpath, zippath, ignoreDirOrFile)
        if isUploadOss:
            uploadoss(zippath, ossBakPath)
        if isRemoveBak and isUploadOss:
            os.remove(zippath)
    # uploadoss('D:/webbak/zhaokeli.com-2019-06-12_16-31-24.zip', 'webbak/')
    # input('...')
