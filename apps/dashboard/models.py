from django.db import models

# Create your models here.

class ProTable(models.Model):
    member_id = models.CharField(max_length=45)
    file_name = models.TextField()
    new_file_name = models.TextField()
    trans_dtime = models.TextField()
    trans_md = models.CharField(max_length=3)
    ats_kdcd_dtl = models.TextField()
    ori_text = models.TextField()
    pro_text = models.TextField()
    first_tag = models.CharField(max_length=10, blank=True, null=True)
    second_tag = models.CharField(max_length=10, blank=True, null=True)
    event_dtime = models.TextField()
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pro_table'

class ModTable(models.Model):
    pro_table = models.ForeignKey('ProTable', models.DO_NOTHING)
    member_id = models.CharField(max_length=45)
    event_dtime = models.TextField()
    file_name = models.TextField()
    ori_text = models.TextField()
    first_tag = models.CharField(max_length=10)
    second_tag = models.CharField(max_length=10)
    mod_first_tag = models.CharField(max_length=10)
    mod_second_tag = models.CharField(max_length=10)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mod_table'
