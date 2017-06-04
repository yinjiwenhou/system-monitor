import os

from django.shortcuts import render
from django.http import HttpResponse
from os_msg import get_cpu_usage, get_cpu_count
from os_msg import get_mem_usage, get_mem
from os_msg import get_os_process

def cpu_info(request):
    context = {}
    context['cpu_usage'] = get_cpu_usage()
    context['cpu_count'] = get_cpu_count()
    context['mem_usage'] = get_mem_usage()
    return render(request, 'os_info.html', context)

def os_process(request):
    context = {}
    context['data'] = get_os_process()
    return render(request, 'os_process.html', context)

def mem_info(request):
    response = HttpResponse()
    response['Content-Type'] = "text/json"
    response.write(get_mem())
    return response
