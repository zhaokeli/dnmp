# 镜像名字
imageName=mokuyu/composer2

# 构建
docker build . -t ${imageName}

# 登陆
docker login --username=735579768@qq.com registry.cn-beijing.aliyuncs.com

# push
imageId=`docker images -q ${imageName}`
docker tag ${imageId} registry.cn-beijing.aliyuncs.com/${imageName}:latest
docker push registry.cn-beijing.aliyuncs.com/${imageName}:latest

#拉取并重命名镜像
docker pull registry.cn-beijing.aliyuncs.com/mokuyu/composer2
docker tag `docker images -q registry.cn-beijing.aliyuncs.com/mokuyu/composer2` mokuyu/composer2