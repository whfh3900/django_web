from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import DataTable, AuthUser, ProTable
from django.http import JsonResponse, FileResponse
from django.core.files.storage import FileSystemStorage

import pandas as pd
#import logging
#from tabulate import tabulate
import time
# Create your views here.
from ats_module.TextPreprocessing import *
from ats_module.TextTagging import *
import datetime



@csrf_exempt
def home(request):
    return render(request, 'UI-MA-00-00.html')



@csrf_exempt
def ats_login(request):
    if request.method == "GET":
        logout(request)
        return render(request, "UI-AT-JO-00.html")
    
    elif request.method == "POST":
        userID = request.POST['userID']
        password = request.POST['password']
        user = authenticate(request, username=userID, password=password)
        global context

        try:

            if user is not None:    
                login(request, user)
                data_list = DataTable.objects.filter(member_id=userID).values('new_file_name','pro_dtime','data_len','pro_result')
                name = list(AuthUser.objects.filter(username=userID).values('first_name','last_name'))[0]
                name = name['first_name']+name['last_name']
                context = {'data_list':data_list, 'userID':userID, 'name':name, 'data_len':len(data_list)}
                # Redirect to a success page.
                return render(request, 'UI-AT-DA-00.html', context)

            else:
                # Return an 'invalid login' error message.
                context['error'] = 'Not found ID or PW!'
                return render(request, "UI-AT-JO-00.html", context)

        except Exception as e:
            context['error'] = 'Please write ID or PW!'
            return render(request, "UI-AT-JO-00.html", context)
            

@csrf_exempt
def tagging(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, 'UI-AT-DA-00.html')

        elif request.method == "POST":
            file = request.FILES.get("testFile")
            userID = context["userID"]
            file_name = request.POST["filename"]

            for chunk in file.chunks():
                try:
                    file_chunk = chunk.decode('utf-8-sig')
                except UnicodeDecodeError:
                    error_log = "다음의 인코딩 형식을 지원합니다. <b>(utf-8)</b>"
                    return JsonResponse({"error": error_log}, status=403)

            
            chunks = file_chunk.replace('\r\n', ',')
            chunk_list = chunks.split(',')[:-1]
            columns = chunk_list[0:3]

            true_columns = ["거래구분","거래유형","적요"]

            for i,n in enumerate(columns):
                if n not in true_columns:
                    error_log = "%s 컬럼이 없습니다. 데이터 형식을 확인하세요.<br><b>(필수컬럼: %s) 에러->%s</b>"%(true_columns[i], str(true_columns), n)
                    return JsonResponse({"error": error_log}, status=403)

            chunk_list = chunk_list[3:]
            data_len = int(round(len(chunk_list)/3, 0))
            
            if data_len > 1000000:
                error_log = "<b>1000000건</b> 이내만 처리 가능합니다.<br>파일을 다시 업로드 하세요."
                return JsonResponse({"error": error_log}, status=403)

            new_file_name = file_name.split('.')[0]+'_'+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.csv'

            df = pd.DataFrame(columns=["index","거래구분","원적요","전처리적요","대분류","중분류","비고"])
            
            nk = Nickonlpy()
            nwt = NicWordTagging()
            trans_md = False
            stat = '정상'

            for i,n in enumerate(chunk_list):
                df.at[int(i/3), "index"] = int(i/3)
                if i%3 == 0:
                    if n in ['1', '2']:
                        trans_md = n
                        df.at[int(i/3), "거래구분"] = n

                if i%3 == 2:
                
                    protable = ProTable()
                    protable.member_id = userID
                    protable.file_name = file_name
                    protable.new_file_name = new_file_name
                    protable.trans_md = trans_md
                    protable.ori_text = n
                    df.at[int(i/3), "원적요"] = n

                    # preprocessing
                    text = find_null(n)
                    text = ascii_check(text)
                    text = corporatebody(text)
                    text = remove_specialchar(text)
                    text = numbers_check(text)
                    text = find_null(text)
                    text = nk.predict_tokennize(text)
                    protable.pro_text = text
                    df.at[int(i/3), "전처리적요"] = text                
                    
                    
                    #######################################                
                    if (trans_md) and (text not in ["", " ", "  "]):
                        # tagging
                        result = nwt.text_tagging(text, trans_md)

                        protable.first_tag = result[0]
                        protable.second_tag = result[1]
                        df.at[int(i/3), "대분류"] = result[0]
                        df.at[int(i/3), "중분류"] = result[1]
                        trans_md = False

                    elif (trans_md) and (text in ["", " ", "  "]):
                        stat = '공백'
                        protable.first_tag = "공백"
                        protable.second_tag = "공백"
                        df.at[int(i/3), "대분류"] = ""
                        df.at[int(i/3), "중분류"] = ""
                        protable.note = "200"
                        df.at[int(i/3), "비고"] = "[200]" # 해당하는 데이터가 없을때 발생하는 코드

                    else:
                        stat = '에러'
                        protable.first_tag = ""
                        protable.second_tag = ""
                        df.at[int(i/3), "대분류"] = ""
                        df.at[int(i/3), "중분류"] = ""
                        protable.note = "333"
                        df.at[int(i/3), "비고"] = "[333]" # 요청위치 값의 타입이 유효하지 않을 때 발생하는 코드


                    protable.event_dtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    protable.note = "000"
                    df.at[int(i/3), "비고"] = "[000]" # 정상작동


                    protable.save()

            df.to_csv('./save/%s'%new_file_name, encoding="utf-8-sig", index=False)

            datatable = DataTable()
            datatable.member_id = userID
            datatable.file_name = file_name
            datatable.new_file_name = new_file_name
            datatable.pro_dtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            datatable.data_len = str(data_len)+'건'
            datatable.pro_result = stat
            datatable.save()

            return JsonResponse({"message":"데이터 처리가 완료되었습니다.<br><b>파일</b>을 다운로드하세요.", "filename":new_file_name}, status=200)
    else:
            return JsonResponse({"message":"please login!"}, status=200)
        
@csrf_exempt
def complete_download(request):
    if request.method == "GET":
        return render(request, 'UI-AT-DA-00.html')

    elif request.method == "POST":
        new_file_name = request.POST["new_file_name"]
        file_path = os.path.dirname('./save/%s'%new_file_name) 
        file_name = os.path.basename('./save/%s'%new_file_name)

        fs = FileSystemStorage(file_path)
        response = FileResponse(fs.open(file_name, 'rb'),
                                content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(new_file_name)
        return response

@csrf_exempt
def history_download(request):
    if request.method == "GET":
        return render(request, 'UI-AT-DA-00.html')

    elif request.method == "POST":
        history_file_name = request.POST["history_file_name"]
        file_path = os.path.dirname('./save/%s'%history_file_name) 
        file_name = os.path.basename('./save/%s'%history_file_name)

        
        fs = FileSystemStorage(file_path)
        response = FileResponse(fs.open(file_name, 'rb'),
                                content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(history_file_name)
        return response


@csrf_exempt
def introduction_download(request):
    if request.method == "GET":
        return render(request, 'UI-MA-00-00.html')

    elif request.method == "POST":
        
        file_path = os.path.dirname('./file/') 
        file_name = os.path.basename('소개서.pdf')
        fs = FileSystemStorage(file_path)
        response = FileResponse(fs.open(file_name, 'rb'))
        response['Content-Disposition'] = 'attachment; filename="{}"'.format('소개서.pdf')
        return response
