# Create your views here.
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from .models import DataTable, AuthUser
from django.http import JsonResponse, FileResponse
from django.core.files.storage import FileSystemStorage, default_storage
# from django.contrib import messages

import os
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

        if user is not None:
            login(request, user)
            data_list = DataTable.objects.filter(member_id=userID).values('new_file_name', 'start_dtime', 'end_dtime',
                                                                          'data_len', 'pro_result')
            name = list(AuthUser.objects.filter(username=userID).values('first_name', 'last_name'))[0]
            name = name['first_name'] + name['last_name']
            context = {'data_list': data_list, 'userID': userID, 'name': name, 'data_len': len(data_list)}
            # Redirect to a success page.
            return render(request, 'UI-AT-DA-00.html', context)

        else:
            # Return an 'invalid login' error message.
            return render(request, "UI-AT-JO-01.html")


@csrf_exempt
def tagging(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, 'UI-AT-DA-00.html')

        elif request.method == "POST":
            file = request.FILES["testFile"]
            userID = context["userID"]
            file_name = request.POST["filename"]
            path = default_storage.save(file.name, file)

            try:
                # media 폴더에 저장
                chunks = default_storage.open(path).read().decode('utf-8-sig')
            except UnicodeDecodeError as e:
                # time.sleep(0.5)
                error_log = "다음의 인코딩 형식을 지원합니다.(utf-8) %s" % e
                response = JsonResponse({"success": False, "error": error_log})
                response.status_code = 403
                return response

            # media 폴더에 저장된 파일 바로삭제
            # default_storage.delete(path)
            chunks = chunks.replace('\r\n', ',')
            chunk_list = chunks.split(',')[:-1]
            columns = chunk_list[0:3]
            true_columns = ["거래구분", "거래유형", "적요"]

            # 데이터 컬럼형식 검사 ###########################################
            for i, n in enumerate(columns):
                if n != true_columns[i]:
                    # time.sleep(0.5)
                    error_log = "<li>%s 컬럼이 없습니다. 데이터 형식을 확인하세요.</li><li>(컬럼순서: %s) </li><li>에러컬럼 : %s</li>" % (
                        true_columns[i], str(true_columns), n)
                    response = JsonResponse({"success": False, "error": error_log})
                    response.status_code = 403
                    return response
            ###############################################################

            # 데이터 길이 검사 ##############################################
            chunk_list = chunk_list[3:]
            data_len = int(round(len(chunk_list) / 3, 0))
            if data_len > 1000000:
                # time.sleep(0.5)
                error_log = "1000000건 이내만 처리 가능합니다. 파일을 다시 업로드 하세요."
                response = JsonResponse({"success": False, "error": error_log})
                response.status_code = 403
                return response
            ###############################################################

            new_file_name = file_name.split('.')[0] + '_' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '.csv'

            # 태깅전 data table 입력
            datatable = DataTable()
            datatable.member_id = userID
            datatable.file_name = file_name
            datatable.new_file_name = new_file_name
            datatable.start_dtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            datatable.data_len = str(data_len) + '건'
            datatable.pro_result = '진행중'
            datatable.save()


            # 이전버젼 ##############################################
            # df = pd.DataFrame(columns=["index", "거래구분", "거래유형", "적요", "대분류", "중분류", "비고"])
            # nk = Nickonlpy()
            # nwt = NicWordTagging()
            # trans_md = False
            # ats_kdcd_dtl = False
            # for i,n in enumerate(tqdm(chunk_list)):
            #     df.at[int(i/3), "index"] = int(i/3)
            #     if i%3 == 0:
            #         df.at[int(i / 3), "거래구분"] = n
            #         if n in ['1', '2']:
            #             trans_md = n
            #         else:
            #             trans_md = 'e'
            #
            #     if i%3 == 1:
            #         df.at[int(i / 3), "거래유형"] = n
            #         ats_kdcd_dtl = n
            #
            #     if i%3 == 2:
            #         protable = ProTable()
            #         protable.member_id = userID
            #         protable.file_name = file_name
            #         protable.new_file_name = new_file_name
            #         protable.trans_md = trans_md
            #         protable.ats_kdcd_dtl = ats_kdcd_dtl
            #         protable.ori_text = n
            #         df.at[int(i/3), "적요"] = n
            #
            #         # preprocessing
            #         text = find_null(n)
            #         text = ascii_check(text)
            #         text = change_upper(text)
            #         text = space_delete(text)
            #         text = remove_bank(text)
            #         text = corporatebody(text)
            #         text = numbers_to_zero(text)
            #         text = remove_specialchar(text)
            #         text = nk.predict_tokennize(text)
            #
            #         # 정상일때 #######################################
            #         if (trans_md != 'e') and (text not in ["", " ", "  "]):
            #             # tagging
            #             result = nwt.text_tagging(text, trans_md)
            #             text = nk.name_check(text)
            #             protable.pro_text = text
            #             protable.first_tag = result[0]
            #             protable.second_tag = result[1]
            #             df.at[int(i/3), "대분류"] = result[0]
            #             df.at[int(i/3), "중분류"] = result[1]
            #             trans_md = False
            #             protable.note = "000"
            #
            #         # 적요가 공백일때 #################################
            #         elif (trans_md != 'e') and (text in ["", " ", "  "]):
            #             protable.pro_text = text
            #             protable.first_tag = "공백"
            #             protable.second_tag = "공백"
            #             df.at[int(i/3), "대분류"] = ""
            #             df.at[int(i/3), "중분류"] = ""
            #             protable.note = "200"
            #
            #         # 거래구분이 이상할 때 ############################
            #         elif trans_md == 'e':
            #             protable.pro_text = text
            #             protable.first_tag = ""
            #             protable.second_tag = ""
            #             df.at[int(i/3), "대분류"] = ""
            #             df.at[int(i/3), "중분류"] = ""
            #             protable.note = "333"
            #
            #         protable.event_dtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #         protable.save()
            # df.to_csv('./save/%s' % new_file_name, encoding="utf-8-sig", index=False)
            ###############################################################


            # 현재버젼 ##############################################
            try:
                os.system('python work_func.py %s %s %s' % (userID, file_name, new_file_name))
                if os.path.exists('./media/%s' % file_name):
                    os.remove('./media/%s' % file_name)

            except Exception as e:
                print(e)
                if os.path.exists('./media/%s' % file_name):
                    os.remove('./media/%s' % file_name)
            ###############################################################

            # 태깅후 data table 입력
            datatable.end_dtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            datatable.pro_result = '완료'
            datatable.save()

            return JsonResponse({"message": "데이터 처리가 완료되었습니다. 파일을 다운로드하세요.", "filename": new_file_name}, status=200)
    else:
        return JsonResponse({"message": "please login!"}, status=200)


@csrf_exempt
def complete_download(request):
    if request.method == "GET":
        return render(request, 'UI-AT-DA-00.html')

    elif request.method == "POST":
        new_file_name = request.POST["new_file_name"]
        file_path = os.path.dirname('./save/%s' % new_file_name)
        file_name = os.path.basename('./save/%s' % new_file_name)

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
        file_path = os.path.dirname('./save/%s' % history_file_name)
        file_name = os.path.basename('./save/%s' % history_file_name)

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
        fs = FileSystemStorage(os.path.dirname('./'))
        response = FileResponse(fs.open('file.pdf', 'rb'))
        response['Content-Disposition'] = 'attachment; filename="{}"'.format('다운로드.pdf')
        return response


