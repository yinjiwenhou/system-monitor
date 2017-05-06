from django.shortcuts import render
from os_msg import get_cpu_usage, get_cpu_count
from os_msg import get_mem_usage

def cpu_info(request):
    context = {}
    context['cpu_usage'] = get_cpu_usage()
    context['cpu_count'] = get_cpu_count()
    context['mem_usage'] = get_mem_usage()
    return render(request, 'os_info.html', context)
