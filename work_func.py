# -*- coding: utf-8 -*-
import sys
import os
import platform
# import site
# raise Exception(site.getsitepackages())

import django
# if platform.system() == 'Windows':
#     sys.path.append('C:\\Users\\choi seung un\\niccompany\\2022년_상품개발\\code\\git\\django_web')
# elif platform.system() == 'Linux':
#     sys.path.append('/home/manager/django_web')
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ats.settings')
django.setup()
import pandas as pd
import numpy as np
from tagging.models import ProTable

from tqdm import tqdm
from ats_module.TextPreprocessing import *
from ats_module.TextTagging import *
import multiprocessing
import datetime

if platform.system() == 'Windows':
    from multiprocessing import Pool
elif platform.system() == 'Linux':
    from multiprocessing.pool import ThreadPool as Pool

# global value #############################
userID = sys.argv[1]
file_name = sys.argv[2]
new_file_name = sys.argv[3]
if platform.system() == 'Windows':
    read_path = './media/%s' % file_name
elif platform.system() == 'Linux':
    read_path = '/home/manager/django_web/media/%s' % file_name
df = pd.read_csv(read_path, encoding='utf-8-sig')

df["대분류"] = np.nan
df["중분류"] = np.nan
df["비고"] = np.nan
# print(df.to_string())

nk = Nickonlpy()
nwt = NicWordTagging()
protable = ProTable()
############################################

def work_func(df):
    for i, n in tqdm(df.iterrows()):
        ori_text = str(n['적요'])
        trans_md = str(n['거래구분'])
        ats_kdcd_dtl = str(n['거래유형'])
        pro_text = ""
        protable.ori_text = ori_text
        protable.trans_md = trans_md
        protable.ats_kdcd_dtl = ats_kdcd_dtl

        if trans_md in ['1', '2']:
            # preprocessing
            pro_text = find_null(ori_text)
            pro_text = ascii_check(pro_text)
            pro_text = change_upper(pro_text)
            pro_text = space_delete(pro_text)
            pro_text = remove_bank(pro_text)
            pro_text = corporatebody(pro_text)
            pro_text = numbers_to_zero(pro_text)
            pro_text = remove_specialchar(pro_text)

            # 문의
            pro_text = space_delete(pro_text)
            pro_text = find_null(pro_text)

            if (pro_text != "공백") or (len(pro_text) >= 1):
                # tagging
                pro_text = nk.predict_tokennize(pro_text)
                result = nwt.text_tagging(pro_text, trans_md)
                pro_text = nk.name_check(pro_text)
                note = "000"
            else:
                result = ("", "")
                note = "200"
        else:
            result = ("", "")
            note = "333"

        df.at[i, "대분류"] = result[0]
        df.at[i, "중분류"] = result[1]
        event_dtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        protable.pro_text = pro_text
        protable.first_tag = result[0]
        protable.second_tag = result[1]
        protable.event_dtime = event_dtime
        protable.note = note
        protable.save()

    return df


def parallel_dataframe(df, func, num_cores):
    df_split = np.array_split(df, num_cores)
    pool = Pool(num_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df


if __name__ == '__main__':
    if platform.system() == 'Windows':
        multiprocessing.freeze_support()
        save_path = './save/%s' % new_file_name
    elif platform.system() == 'Linux':
        save_path = '/home/manager/django_web/save/%s' % new_file_name
    else:
        save_path = '/home/manager/django_web/save/%s' % new_file_name

    num_cores = 8
    df = parallel_dataframe(df, work_func, num_cores)
    df.to_csv(save_path, encoding='utf-8-sig')
    del df


