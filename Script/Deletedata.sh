#!/bin/bash

# ---------- Custom Config Option ----------
expire_days=30
id="root"
pw="Slrzja13@$"
db="ATS"
table="data_table"
column="end_dtime"
# -----------------------------------------------


echo "Start Deletedata.sh"
mysql -u ${id} -p ${pw} ${db} -e " delete from ${table} where ${column} < date_add(date_format(now(), '%Y-%m-%d'), interval ${expire_days} day);"
echo "End Deletedata.sh"


# Crontab -------------------------------------
#crontab -e
#00 00 * * * /home/manager/Script/Deletedata.sh
# -----------------------------------------------
