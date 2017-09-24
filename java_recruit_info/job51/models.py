from django.db import models
# Create your models here.

# 职位类
class Job(models.Model):
    job_id = models.IntegerField(primary_key=True)
    job_name = models.CharField(max_length=100)
    job_company_name = models.CharField(max_length=200)
    job_area_name = models.CharField(max_length=50)
    job_salary = models.CharField(max_length=50)

# 职位详情类
class JobDetail(models.Model):
    job_detail_id = models.AutoField(primary_key=True)
    job_company_type = models.CharField(max_length=100)
    job_publish_time = models.CharField(max_length=20)
    job_address = models.CharField(max_length=100)
    job_company_scale = models.CharField(max_length=100)
    job_require_other = models.CharField(max_length=100)
    job_description = models.TextField(blank=True)
    job_position_tag = models.CharField(max_length=1000)
    job_welfare = models.CharField(max_length=1000)
    job_cleaned_description = models.TextField(blank=True)
    job = models.ForeignKey(Job)

# 分词统计类
class SegmentCount(models.Model):
    segment_count_id = models.AutoField(primary_key=True)
    job_id = models.IntegerField()
    key_word = models.CharField(max_length=100)
    count =  models.IntegerField()


