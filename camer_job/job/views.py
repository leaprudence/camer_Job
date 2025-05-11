from django.shortcuts import render
from .models import Task, Domain
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import User
from django.shortcuts import render, redirect




def index(request, *args, **kwargs):
    task_list = Task.objects.order_by('-id')[:4]
    domain_list = Domain.objects.all()
    context = {
     'task_list' : task_list,
     'domain_list' : domain_list,
        }
    return render(request, 'job/index.html', context)



def home(request, *args, **kwargs):
    tasks = Task.objects.all()
    context = {
        'tasks' : tasks
    }
    return render(request, 'job/home.html', context)

def myJobs(request, *args, **kwargs):
    return render(request, 'job/myJobs.html')

class CreateJob(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'job/createJob.html')

    def post(self, request, *args, **kwargs):
        return HttpResponse('POST request!')