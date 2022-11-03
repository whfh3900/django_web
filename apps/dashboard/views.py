from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import ProTable, ModTable
from apps.tagging.models import DataTable
import datetime
from django.contrib import messages

# Create your views here.
@csrf_exempt
def board(request):
    return render(request, 'UI-DB-00-00.html')


@csrf_exempt
def filelist(request):
    if request.user.is_authenticated:
        userID = str(request.user)
        if request.method == "GET":
            dashboard_data_list = DataTable.objects.filter(member_id=userID, pro_result="완료").values('id', 'file_name',
                                                                                                        'new_file_name',
                                                                                                        'start_dtime',
                                                                                                        'end_dtime')
            context = {"dashboard_data_list": dashboard_data_list}
            return render(request, 'UI-DB-01-00.html', context)

        elif request.method == "POST":
            new_file_name = request.POST["new_file_name"]
            dashboard_data_list = DataTable.objects.filter(member_id=userID, pro_result="완료").values('id', 'file_name',
                                                                                                        'new_file_name',
                                                                                                        'start_dtime',
                                                                                                        'end_dtime')
            dashboard_pro_list = ProTable.objects.filter(member_id=userID, new_file_name=new_file_name).values('id',
                                                                                                               'file_name',
                                                                                                               'trans_dtime',
                                                                                                               'trans_md',
                                                                                                               'ats_kdcd_dtl',
                                                                                                               'ori_text',
                                                                                                               'first_tag',
                                                                                                               'second_tag')

            context = {"dashboard_data_list": dashboard_data_list, "dashboard_pro_list": dashboard_pro_list}
            return render(request, 'UI-DB-01-00.html', context)
    else:
        return render(request, 'page-401.html')

@csrf_exempt
def modify(request):
    if request.user.is_authenticated:
        userID = str(request.user)
        global status
        if request.method == "GET":
            dashboard_data_list = DataTable.objects.filter(member_id=userID, pro_result="완료").values('id',
                                                                                                     'file_name',
                                                                                                     'new_file_name',
                                                                                                     'start_dtime',
                                                                                                     'end_dtime')
            if status:
                messages.success(request, '저장완료')
                status = False
            return render(request, 'UI-DB-01-00.html', {"dashboard_data_list": dashboard_data_list})


        elif request.method == "POST":
            modData = request.POST["modData"].split(',')
            mod_first_tag = request.POST["mod_first_tag"]
            mod_second_tag = request.POST["mod_second_tag"]

            modtable = ModTable()
            modtable.pro_table_id = modData[0]
            modtable.member_id = userID
            modtable.event_dtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            modtable.file_name = modData[1]
            modtable.ori_text = modData[2]
            modtable.first_tag = modData[3]
            modtable.second_tag = modData[4]
            modtable.mod_first_tag = mod_first_tag
            modtable.mod_second_tag = mod_second_tag
            modtable.save()
            status = True
            return redirect('.')
    else:
        return render(request, 'page-401.html')
