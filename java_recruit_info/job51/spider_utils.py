#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from pyquery import PyQuery as pq
import re


# http://m.51job.com/ajax/search/joblist.ajax.php?keyword=java&keywordtype=2&pageno=4
URL_51JOB_List = 'http://m.51job.com/ajax/search/joblist.ajax.php'

# http://m.51job.com/search/jobdetail.php?jobtype=0&jobid=84286777
URL_51JOB_DETAIL = 'http://m.51job.com/search/jobdetail.php'

USER_AGENT = 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 ' \
             '(KHTML, like Gecko) Chrome/60.0.3112.78 Mobile Safari/537.36'

# 51job列表页面url处理
class JobListRequest():
    def __init__(self,keyword = 'java',keywordtype=2,pageno = 1,jobarea='080200'):
        self.keyword = keyword
        self.keywordtype = keywordtype
        self.pageno = pageno
        self.jobarea = jobarea

    def setPageNo(self,pageno):
        self.pageno = pageno

    def setJobArea(self,jobarea):
        self.jobarea = jobarea

    def get_return_json(self):
        headers = {
            'User-Agent': USER_AGENT
        }
        response = requests.get(URL_51JOB_List ,headers=headers,
            params={'keyword':self.keyword, 'keywordtype':self.keywordtype, 'pageno':self.pageno, 'jobarea':self.jobarea })
        response.encoding = 'utf-8'
        data = response.json()
        if data != None:
            return  data['data']
        else:
            return None


# 51job详情页面url处理
class JobDetailRequest():
    def __init__(self,jobid,jobtype = 0):
        if jobid == None or int(jobid) < 1:
            raise ValueError("jobId必填且大于0的整数！")

        self.jobid = jobid
        self.jobtype = jobtype

    def setJobId(self,jobid):
        self.jobid = jobid

    def get_ret_text(self):
        headers = {
            'User-Agent': USER_AGENT
        }
        response = requests.get(URL_51JOB_DETAIL,headers=headers,
            params={'jobid': self.jobid, 'jobtype': self.jobtype},)
        response.encoding = 'utf-8'
        data = response.text
        if response.status_code == 200:
            return response.text
        else:
            return None


class JobDetailHandler():
    def __init__(self,html):
        self.html = html

    def get_handler_result(self):
        doc = pq(self.html)
        ret = dict()
        ret['job_company_type'] = doc('.wp .xq .xqd .at span').filter(lambda i,this: pq(this).text() == '性质').parent().text().replace("性质","")
        ret['job_publish_time'] = doc('.wp .xq .xqd .at span').filter(lambda i,this: pq(this).text() == '发布').parent().text().replace("发布","")
        ret['job_address'] = doc('.wp .xq .xqd .at span').filter(lambda i,this: pq(this).text() == '地区').parent().text().replace("地区","")
        ret['job_company_scale'] = doc('.wp .xq .xqd .at span').filter(lambda i,this: pq(this).text() == '规模').parent().text().replace("规模","")
        ret['job_require_other'] = doc('.wp .xq .xqd span').filter(lambda i,this: pq(this).text() == '招聘').parent().text().replace("招聘","")
        ret['job_description'] = doc('.mtb article').text()

        # 职位描述字段数据清洗
        ret['job_cleaned_description'] = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、【】“”：；（）《》‘’{}？！⑦()、%^>℃：~@#￥%……&*（）]+"," ", ret['job_description']).lower()

        ret['job_position_tag'] = doc('.mtb .t3').parents(".sb").next().children().text()
        ret['job_welfare'] = doc('.mtb .t4').parents(".sb").next().children().text()
        return  ret


# if __name__ == '__main__' :
#     with open("resource/job51_template_html.txt",'r',encoding='utf-8') as f:
#         spider_html_template =  f.read()
#         r = JobDetailHandler(spider_html_template)
#         r2 = r.get_handler_result()
#         r3 = r2['job_cleaned_description']
#         items = word_count(r3)
#         if items != None and len(items) > 0:
#             for item in items:
#                 print("kew_word: %s   count: %s" %(item[0],item[1]))
#         # r = JobListRequest()
#         # r.get_return_json()
