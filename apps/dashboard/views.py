from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ProTable, ModTable
from apps.tagging.models import DataTable
import datetime
from django.contrib import messages
from django.db.models import Max
import pandas as pd
import json
# Create your views here.
@csrf_exempt
def board(request):
    if request.user.is_authenticated:
        userID = str(request.user)
        context = dict()
        last_file = DataTable.objects.filter(member_id=userID).aggregate(new_file_name=Max('new_file_name'))['new_file_name']
        data = ProTable.objects.filter(member_id=userID, new_file_name=last_file).values('id', 'trans_dtime', 'trans_md',
                                                                                         'ats_kdcd_dtl', 'ori_text',
                                                                                         'first_tag', 'second_tag')
        data = pd.DataFrame(list(data))
        if len(data) == 0:
            render(request, 'UI-DB-00-00.html', context)
        else:
            data['trans_dtime'] = pd.to_datetime(data['trans_dtime'], format='%Y-%m-%d %H:%M', errors='raise')
            year = data['trans_dtime'].dt.year.max()
            data = data[data['trans_dtime'].between('%s-01-01'%year, '%s-12-31'%year)]
            data['month'] = data['trans_dtime'].dt.month
            de_data = data[data['trans_md'] == '2'].copy()
            ex_data = data[data['trans_md'] == '1'].copy()

            all_time_groupby = data.groupby('month')['id'].count().add_suffix('월').reset_index()
            de_time_groupby = de_data.groupby('month')['id'].count().add_suffix('월').reset_index()
            ex_time_groupby = ex_data.groupby('month')['id'].count().add_suffix('월').reset_index()

            context['all_time_line_labels'] = all_time_groupby['month'].tolist()
            context['all_time_line_data'] = all_time_groupby['id'].tolist()
            context['ex_time_line_labels'] = ex_time_groupby['month'].tolist()
            context['ex_time_line_data'] = ex_time_groupby['id'].tolist()
            context['de_time_line_labels'] = de_time_groupby['month'].tolist()
            context['de_time_line_data'] = de_time_groupby['id'].tolist()

            de_first_tag_groupby = de_data.groupby('first_tag')['id'].count().add_suffix('').reset_index()
            ex_first_tag_groupby = ex_data.groupby('first_tag')['id'].count().add_suffix('').reset_index()

            context['de_first_tag_data'] = de_first_tag_groupby['id'].tolist()
            context['de_first_tag_labels'] = de_first_tag_groupby['first_tag'].tolist()
            context['ex_first_tag_data'] = ex_first_tag_groupby['id'].tolist()
            context['ex_first_tag_labels'] = ex_first_tag_groupby['first_tag'].tolist()

            context['입금'] = dict()
            context['출금'] = dict()
            for i in context['de_first_tag_labels']:
                temp = de_data[de_data['first_tag'] == i]
                context['입금'][i] = temp.groupby('second_tag')['id'].count().to_dict()

            for i in context['ex_first_tag_labels']:
                temp = ex_data[ex_data['first_tag'] == i]
                context['출금'][i] = temp.groupby('second_tag')['id'].count().to_dict()


            # return JsonResponse(data=context, status=200)
            return render(request, 'UI-DB-00-00.html', context)
            # return HttpResponse(json.dumps(context, ensure_ascii=False), content_type=u"application/json; charset=utf-8")
    else:
        return render(request, 'page-401.html')

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
