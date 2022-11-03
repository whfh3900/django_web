# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CorpusDictionary(models.Model):
    word = models.TextField()
    tag = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'corpus_dictionary'


class DataTable(models.Model):
    member_id = models.CharField(max_length=45)
    file_name = models.TextField()
    new_file_name = models.TextField()
    start_dtime = models.TextField()
    end_dtime = models.TextField()
    data_len = models.TextField()
    pro_result = models.CharField(max_length=3)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_table'
