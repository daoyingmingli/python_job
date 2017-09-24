from django.conf.urls import url
from django.views.decorators.cache import cache_page
from . import views

app_name = 'job51'
urlpatterns = [
    url(r'^$', views.job_list, name='job_list'),
    url(r'^job/list/$', views.job_list, name='job_list'),
    url(r'^job/list/ajax/$', views.job_list_ajax, name='job_list_ajax'),
    url(r'^job/detail/(?P<job_id>\d+)$', views.job_detail, name='job_detail'),
    url(r'^job/keyword/(?P<job_id>\d+)$', views.job_keyword, name='job_keyword'),
    url(r'^job/segment_count_sum/$', views.segment_count_sum, name='segment_count_sum'),
    url(r'^job/segment_count_sum/ajax/$', views.segment_count_sum_ajax, name='segment_count_sum_ajax'),
    url(r'^job/segment_count_sum/chart/$', views.segment_count_sum_chart, name='segment_count_sum_chart'),
]