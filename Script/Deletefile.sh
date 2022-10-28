#!/bin/bash


# ---------- Custom Config Option ----------

log_path="/home/manager/django_web/logs"
save_path="/home/manager/django_web/save"
expire_days=30

# -----------------------------------------------


echo "Start Deletefile.sh"
find ${log_path}/* -type f -mtime +${expire_days} -exec rm -f {} \;
find ${save_path}/*.csv -type f -mtime +${expire_days} -exec rm -f {} \;
echo "End Deletefile.sh"


# Crontab -------------------------------------
#crontab -e
#00 00 * * * /home/manager/django_web/Script/Deletefile.sh
# -----------------------------------------------
