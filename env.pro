#
# PHP source directory
#
SOURCE_DIR=./www

#
# Runtime data directory
#
DATA_DIR=./data

#
# Container Timezone
#
TZ=Asia/Shanghai

#
# Container package fetch url
#
# Can be empty, followings or others:
# mirrors.163.com
# mirrors.aliyun.com
# mirrors.ustc.edu.cn
#
CONTAINER_PACKAGE_URL=mirrors.aliyun.com

#
# Nginx
#
NGINX_VERSION=1.15.7-alpine
NGINX_HTTP_HOST_PORT=80
NGINX_HTTPS_HOST_PORT=443
NGINX_CONFD_DIR=./services/nginx/conf.d
NGINX_CONF_FILE=./services/nginx/nginx.conf
NGINX_FASTCGI_PHP_CONF=./services/nginx/fastcgi-php.conf
NGINX_FASTCGI_PARAMS=./services/nginx/fastcgi_params
NGINX_SSL_CERTIFICATE_DIR=./services/nginx/ssl
NGINX_LOG_DIR=./logs/nginx
# Available apps: certbot
NGINX_INSTALL_APPS=

#
# Openresty
#
OPENRESTY_VERSION=alpine
OPENRESTY_HTTP_HOST_PORT=80
OPENRESTY_HTTPS_HOST_PORT=443
OPENRESTY_CONFD_DIR=./services/openresty/conf.d
OPENRESTY_CONF_FILE=./services/openresty/openresty.conf
OPENRESTY_FASTCGI_PHP_CONF=./services/openresty/fastcgi-php.conf
OPENRESTY_CONF_FASTCGIPARAMS_FILE=./services/openresty/fastcgi_params
OPENRESTY_SSL_CERTIFICATE_DIR=./services/openresty/ssl
OPENRESTY_LOG_DIR=./logs/nginx

#
# PHP7
#
# Available PHP_EXTENSIONS:
#
# pdo_mysql,zip,pcntl,mysqli,mbstring,exif,bcmath,calendar,
# sockets,gettext,shmop,sysvmsg,sysvsem,sysvshm,pdo_rebird,
# pdo_dblib,pdo_oci,pdo_odbc,pdo_pgsql,pgsql,oci8,odbc,dba,
# gd,intl,bz2,soap,xsl,xmlrpc,wddx,curl,readline,snmp,pspell,
# recode,tidy,gmp,imap,ldap,imagick,sqlsrv,mcrypt,opcache,
# redis,memcached,xdebug,swoole,pdo_sqlsrv,sodium,yaf,mysql,
# amqp,mongodb,event,rar,ast,yac,yaconf,msgpack,igbinary,
# seaslog,varnish,xhprof,ssh2
#
# You can let it empty to avoid installing any extensions,
# or install multi plugins as:
# PHP_EXTENSIONS=pdo_mysql,mysqli,gd,curl,opcache
#
PHP_VERSION=7.2.25
PHP_PHP_CONF_FILE=./services/php/php.ini
PHP_FPM_CONF_FILE=./services/php/php-fpm.conf
PHP_LOG_DIR=./logs/php
PHP_EXTENSIONS=pdo_mysql,mysqli,mbstring,gd,curl,opcache,redis,amqp,mcrypt,swoole,mongodb,ssh2

PHP74_VERSION=7.4
PHP74_PHP_CONF_FILE=./services/php/php4.ini
PHP74_FPM_CONF_FILE=./services/php/php-fpm.conf
PHP74_LOG_DIR=./logs/php
PHP74_EXTENSIONS=pdo_mysql,mysqli,mbstring,gd,curl,opcache,redis,amqp,mcrypt,swoole,mongodb,ssh2
#
# PHP5.6
#
PHP56_VERSION=5.6.40
PHP56_PHP_CONF_FILE=./services/php/php.ini
PHP56_FPM_CONF_FILE=./services/php/php-fpm.conf
PHP56_LOG_DIR=./logs/php
PHP56_EXTENSIONS=pdo_mysql,mysqli,mbstring,gd,curl,opcache,redis,amqp,mcrypt,swoole,mongodb

#
# PHP5.4
#
PHP54_VERSION=5.4.45
PHP54_PHP_CONF_FILE=./services/php54/php.ini
PHP54_FPM_CONF_FILE=./services/php54/php-fpm.conf
PHP54_LOG_DIR=./logs/php
PHP54_EXTENSIONS=pdo_mysql,mysqli,mbstring,gd,curl,opcache

#
# RABBITMQ
#
RABBITMQ_VERSION=management
RABBITMQ_HOST_PORT_C=5672
RABBITMQ_HOST_PORT_S=15672
RABBITMQ_DEFAULT_USER=myuser
RABBITMQ_DEFAULT_PASS=mypass

#
# MONGODB
#
MONGODB_VERSION=4.1
MONGODB_HOST_PORT=27017
MONGODB_INITDB_ROOT_USERNAME=root
MONGODB_INITDB_ROOT_PASSWORD=123456

#
# ELASTICSEARCH
#
# Available ELASTICSEARCH_PLUGINS:
#
# amazon-ec2,analysis-icu,analysis-kuromoji,analysis-nori,
# analysis-phonetic,analysis-smartcn,analysis-stempel,
# analysis-ukrainian,discovery-azure-classic,discovery-ec2,
# discovery-file,discovery-gce,google-cloud-storage,
# ingest-attachment,ingest-geoip,ingest-user-agent,mapper-murmur3,
# mapper-size,microsoft-azure-storage,qa,repository-azure,
# repository-gcs,repository-hdfs,repository-s3,store-smb,
# analysis-ik,analysis-pinyin
#
# You can let it empty to avoid installing any plugins,
# or install plugins as:
# ELASTICSEARCH_PLUGINS=analysis-ik,analysis-pinyin
#
ELASTICSEARCH_VERSION=7.1.1
ELASTICSEARCH_CONF_FILE=./services/elasticsearch/elasticsearch.yml
ELASTICSEARCH_HOST_PORT_C=9200
ELASTICSEARCH_HOST_PORT_S=9300
ELASTICSEARCH_PLUGINS=

#
# KIBANA
#
KIBANA_VERSION=7.1.1
KIBANA_HOST=5601

#
# LOGSTASH
#
LOGSTASH_VERSION=7.1.1
LOGSTASH_HOST=5601
LOGSTASH_HOST_PORT_C=9600
LOGSTASH_HOST_PORT_S=5044

#
# MySQL8
#
MYSQL_VERSION=8.0.13
MYSQL_HOST_PORT=3306
MYSQL_ROOT_PASSWORD=123456
MYSQL_CONF_FILE=./services/mysql/mysql.cnf

#
# MySQL5
#
MYSQL5_VERSION=5.7.28
MYSQL5_HOST_PORT=3306
MYSQL5_ROOT_PASSWORD=123456
MYSQL5_CONF_FILE=./services/mysql5/mysql.cnf

#
# Redis
#
REDIS_VERSION=5.0.3-alpine
REDIS_HOST_PORT=6379
REDIS_CONF_FILE=./services/redis/redis.conf

#
# Memcached
#
MEMCACHED_VERSION=alpine
MEMCACHED_HOST_PORT=11211
MEMCACHED_CACHE_SIZE=128

#
# phpMyAdmin
#
PHPMYADMIN_HOST_PORT=8899
PHPMYADMIN_USER_CONF_FILE=./services/phpmyadmin/config.user.inc.php
PHPMYADMIN_PHP_CONF_FILE=./services/phpmyadmin/php-phpmyadmin.ini

#
# redisMyAdmin
#
REDISMYADMIN_HOST_PORT=8898

#
# AdminMongo
#
ADMINMONGO_HOST_PORT=1234


#
# portainer
#
PORTAINER_HOST_PORT=9090


#
# stunnel-client
#
STUNNEL_CLIENT_NAME=https
STUNNEL_CLIENT_CONNECT_HOST=47.56.171.51
STUNNEL_CLIENT_CONNECT_PORT=4128
STUNNEL_CLIENT_ACCEPT_PORT=8880

#
# stunnel-server
#
STUNNEL_SERVER_NAME=https
STUNNEL_SERVER_CONNECT_HOST=47.56.171.51
STUNNEL_SERVER_CONNECT_PORT=4128
STUNNEL_SERVER_ACCEPT_PORT=8881

#
# scm-manager
#
SCM_MANAGER_PORT=8080

#
# squid
#
SQUID_PORT=3128

#
# ngrok
#
NGROK_HTTP_PORT=8082
NGROK_HTTPS_PORT=8083
NGROK_TUNNEL_PORT=4443
NGROK_DOMAIN=ngrok.59vip.cn