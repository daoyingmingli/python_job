#!/usr/bin/env python
# -*- coding:utf-8 -*-
from .spider_utils import JobListRequest,JobDetailHandler,JobDetailRequest
from .models import Job,JobDetail,SegmentCount
import time
import os
import jieba
import pandas
import numpy

STOP_WORD = pandas.read_csv(os.path.abspath('./job51/resource') + "/stop_words.txt", index_col=False, quoting=3,
                            sep="\t", names=['stopword'], encoding='utf-8')

def query_exist_info_list():
    ret = []
    jobs = Job.objects.all()
    if jobs != None and len(jobs):
        for job in jobs:
            ret.append(job.job_id)
    return ret

 # 统计词频
def word_count(article):
    segment = jieba._lcut(article)
    words_df = pandas.DataFrame({'segment':segment})
    words_df = words_df[words_df.segment.isin(STOP_WORD.stopword)]
    words_stat = words_df.groupby(by=['segment'])['segment'].agg({"count": numpy.size})
    words_stat = words_stat.reset_index().sort_values(by=["count"], ascending=False)
    return  words_stat.values.tolist()

def update_51job():
    count = 1
    exist_job_ids = query_exist_info_list()
    while(True):
        time.sleep(0.5)
        job_list_request = JobListRequest(pageno=count)
        items = job_list_request.get_return_json()
        count = count + 1
        job_list_request.setPageNo(count)
        if(items == None or len(items) == 0):
            break
        else:
            # 遍历java求职网页
            for item in items:
                job_id = item['jobid']
                if int(job_id) not in exist_job_ids:
                    # 保存列表页面
                    exist_job_ids.append(job_id)
                    job_name = item['cjobname']
                    job_company_name = item['cocname']
                    job_area_name = item['jobareaname']
                    job_salary = item['jobsalaryname']
                    job_item = Job(job_id=job_id, job_name=job_name, job_company_name=job_company_name, job_area_name=job_area_name, job_salary=job_salary)
                    job_item.save()

                    # 保存详情页面
                    resp_detail = JobDetailRequest(jobid=job_id)
                    resp_job_detail = JobDetailHandler(resp_detail.get_ret_text())
                    if resp_job_detail:
                        job_detail = resp_job_detail.get_handler_result()

                        job_detail_obj = JobDetail(**job_detail)
                        job_detail_obj.job = job_item
                        job_detail_obj.save()

                        #分词保存
                        try:
                            segments = word_count(job_detail['job_cleaned_description'])
                            if segments and len(segments) > 0:
                                for seg in segments:
                                    if seg and len(seg) == 2 :
                                        segmentCount = SegmentCount(job_id=job_id,key_word=seg[0],count=seg[1])
                                        segmentCount.save()
                        except Exception as e:
                            print(e)