from django.shortcuts import render,HttpResponse
from django.db.models import Sum
from  django.http import JsonResponse
from job51.models import Job,JobDetail,SegmentCount
import json
#获取工作列表
def job_list(request):
    return render(request,template_name="job51/job_list.html")

def job_list_ajax(request):
    jobs = Job.objects.all()
    data = []
    for job in jobs:
        data.append({'job_id': job.job_id, 'job_name': job.job_name, 'job_company_name': job.job_company_name,
                     'job_area_name': job.job_area_name,'job_salary': job.job_salary})
    json_data = json.dumps(data, default= 'utf-8')
    return HttpResponse(json_data)


#获取工作列表
def job_detail(request, job_id):
    detail = JobDetail.objects.filter(job_id=job_id)
    return render(request,template_name="job51/job_detail.html",context={'detail':detail.first()})

#某个职位的关键词信息
def job_keyword(request,job_id):
    keywords  = SegmentCount.objects.filter(job_id=job_id)
    return render(request, template_name="job51/job_keyword.html", context={'keywords': keywords})

#所有的职位的关键词汇总
def segment_count_sum(request):
    jump_to = request.GET.get('jump_to')
    print(jump_to)
    if jump_to and int(jump_to) == 1:
        return render(request, template_name="job51/segment_count_chart.html")
    else:
        return render(request, template_name="job51/segment_count_ajax.html")

def segment_count_sum_ajax(request):
    segs = SegmentCount.objects.values("key_word").annotate(s_count = Sum("count")).order_by("-s_count")
    data = []
    for seg in segs:
        print(seg)
        data.append({'key_word': seg['key_word'], 'count':seg['s_count']})
    json_data = json.dumps(data, default='utf-8')
    return HttpResponse(json_data)

def segment_count_sum_chart(request):
    segs = SegmentCount.objects.values("key_word").annotate(s_count = Sum("count"))
    keys = []
    values = []
    for seg in segs:
        keys.append(seg['key_word'])
        values.append(seg['s_count'])
    return HttpResponse(json.dumps({'keys':keys,'values':values}, default= 'utf-8'))

