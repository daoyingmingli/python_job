# python_job
招聘网站中职位描述的计算机相关词汇的统计；
使用python 以及 django 实现；
使用requests,pyquery从招聘网站爬去招聘信息；
用jieba分词保存到mysql数据库；
前端技术：query,boostrap

抓取数据：
进入django项目;
1） migrate数据库；
2）下载数据：运行以下命令
   python manage.py shell
   from job51 import cron
   cron.update_51job()
 
3）运行：python manage.py runserver
4）在浏览器中访问：http://127.0.0.1:8000
