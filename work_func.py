import sys
import pandas as pd
import numpy as np
import pymysql
import my_settings
from tqdm import tqdm
from ats_module.TextPreprocessing import *
from ats_module.TextTagging import *
from multiprocessing import Pool
import multiprocessing
import datetime
import platform

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

db_info = my_settings.DATABASES['default']
db = pymysql.connect(
    user=db_info['USER'],
    passwd=db_info['PASSWORD'],
    host=db_info['HOST'],
    db=db_info['NAME'],
    charset='utf8'
)
cursor = db.cursor(pymysql.cursors.DictCursor)

nk = Nickonlpy()
nwt = NicWordTagging()
############################################

def work_func(df):
    for i, n in tqdm(df.iterrows()):
        ori_text = str(n['적요'])
        trans_md = str(n['거래구분'])
        ats_kdcd_dtl = str(n['거래유형'])
        pro_text = ""
        note = ""

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
            pro_text = nk.predict_tokennize(pro_text)

            if pro_text not in ["", " ", "  "]:
                # tagging
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
        sql = '''INSERT INTO `pro_table` (member_id, file_name, new_file_name, trans_md, ats_kdcd_dtl, ori_text, pro_text, first_tag, second_tag, event_dtime, note) 
            VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');''' % (userID, file_name, new_file_name, trans_md, ats_kdcd_dtl, ori_text, pro_text, result[0], result[1], event_dtime, note)
        cursor.execute(sql)
        db.commit()
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

    num_cores = 4
    df = parallel_dataframe(df, work_func, num_cores)
    df.to_csv(save_path, encoding='utf-8-sig')
    db.close()


