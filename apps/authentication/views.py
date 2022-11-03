from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from .models import AuthUser
from apps.tagging.models import DataTable
from apps.dashboard.models import ProTable
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage, default_storage
# from django.contrib import messages

import sys
import os
import platform
#
# Create your views here.
@csrf_exempt
def home(request):
    return render(request, 'UI-MA-00-00.html')

@csrf_exempt
def introduction_download(request):
    if request.method == "GET":
        return render(request, 'UI-MA-00-00.html')

    elif request.method == "POST":
        if platform.system() == 'Windows':
            fs = FileSystemStorage(os.path.dirname('./'))
            response = FileResponse(fs.open('file.pdf', 'rb'))
        elif platform.system() == 'Linux':
            file_path = os.path.dirname('/home/manager/django_web/file.pdf')
            file_name = os.path.basename('/home/manager/django_web/file.pdf')
            fs = FileSystemStorage(file_path)
            response = FileResponse(fs.open(file_name, 'rb'))

        response['Content-Disposition'] = 'attachment; filename="{}"'.format('다운로드.pdf')
        return response


@csrf_exempt
def ats_login(request):
    if request.method == "GET":
        logout(request)
        return render(request, "UI-AT-JO-00.html")

    elif request.method == "POST":
        userID = request.POST['userID']
        password = request.POST['password']
        user = authenticate(request, username=userID, password=password)

        if user is not None:
            login(request, user)
            history_list = DataTable.objects.filter(member_id=userID).values('new_file_name', 'start_dtime', 'end_dtime',
                                                                            'data_len', 'pro_result')
            context = {'history_list': history_list, 'history_len': len(history_list)}
            # Redirect to a success page.
            return render(request, 'UI-AT-DA-00.html', context)
            # return render(request, 'base.html', context)

        else:
            # Return an 'invalid login' error message.
            return render(request, "UI-AT-JO-01.html")

@csrf_exempt
def userinfo(request):
    return render(request, 'page-404.html')

@csrf_exempt
def settings(request):
    return render(request, 'page-404.html')
