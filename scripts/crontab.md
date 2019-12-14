# ubuntu 16.0.4
# 每天执行sql备份


# 添加环境变量到crontab -e中,且安装oss2 ,
PYTHONPATH=$PYTHONPATH:/home/[用户名]/.local/lib/python3.5/site-packages

# 执行每天SQL备份任务
0 0 * * * python3 /home/keli/dnmp/scripts/BakSql.py >> ~/dnmp/logs/cron/database.log 2>&1

# 执行每周目录备份任务
0 0 * * 0  python3 /home/keli/dnmp/scripts/BakDir.py >> ~/dnmp/logs/cron/dirdata.log 2>&1