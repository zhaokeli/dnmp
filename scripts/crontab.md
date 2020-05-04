# ubuntu 16.0.4
# 每天执行sql备份
# min   hour    day     month   weekday command
# 添加环境变量到crontab -e中,且安装oss2 ,
PYTHONPATH=$PYTHONPATH:/home/[用户名]/.local/lib/python3.5/site-packages

# 执行每天SQL备份任务
0 0 * * * python3 /home/keli/dnmp/scripts/BakSql.py >> ~/dnmp/logs/cron/database.log 2>&1

# 执行每周目录备份任务
0 0 * * 0  python3 /home/keli/dnmp/scripts/BakDir.py >> ~/dnmp/logs/cron/dirdata.log 2>&1

# bak sql 每天零点执行
0 0 * * * python3 /root/dnmp/scripts/BakSql.py 
# bak mysql5 dir 每天零点执行10分
10 0 * * * python3 /root/dnmp/scripts/Bak-mysql.py 
# bak web dir 每天零点执行
0 0 * * * python3 /root/dnmp/scripts/Bak-web.py 
# bak scm 每周日凌晨3点运行
0 3 * * 0 python3 /root/dnmp/scripts/Bak-scm.py 
# bak gitlab 每周一凌晨2点运行
0 2 * * 1 python3 /root/dnmp/scripts/BakGitLab.py 

# bak gitlab 每周一凌晨3点运行
0 3 * * 1 python3 /root/dnmp/scripts/BakGogs.py 
