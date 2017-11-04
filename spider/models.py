# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class CpuUsage(models.Model):
    hostname = models.CharField(max_length=20)
    cpu_use = models.CharField(max_length=10)
    check_time = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'cpu_usage'


class Csdn(models.Model):
    taskid = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    time = models.CharField(max_length=50)
    content = models.TextField()
    viewnum = models.CharField(max_length=20, blank=True, null=True)
    comment = models.CharField(max_length=10, blank=True, null=True)
    url = models.CharField(max_length=200)
    keywords = models.CharField(max_length=255, blank=True, null=True)
    phrases = models.CharField(max_length=255, blank=True, null=True)
    summary = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'csdn'


class FilesysUsage(models.Model):
    hostip = models.CharField(max_length=20)
    hostname = models.CharField(max_length=30, blank=True, null=True)
    alldisk = models.CharField(max_length=10, blank=True, null=True)
    disk_use = models.CharField(max_length=10, blank=True, null=True)
    disk_free = models.CharField(max_length=10, blank=True, null=True)
    filepath = models.CharField(max_length=10, blank=True, null=True)
    usage = models.CharField(max_length=10, blank=True, null=True)
    check_time = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'filesys_usage'


class Jdproduct(models.Model):
    number = models.AutoField(primary_key=True)
    names = models.CharField(max_length=200)
    url = models.CharField(max_length=250)
    field_id = models.CharField(db_column='_id', max_length=200)  # Field renamed because it started with '_'.
    reallyprice = models.CharField(db_column='reallyPrice', max_length=50)  # Field name made lowercase.
    originalprice = models.CharField(db_column='originalPrice', max_length=50, blank=True, null=True)  # Field name made lowercase.
    favourabledesc1 = models.CharField(db_column='favourableDesc1', max_length=300, blank=True, null=True)  # Field name made lowercase.
    allcount = models.CharField(db_column='AllCount', max_length=50, blank=True, null=True)  # Field name made lowercase.
    goodcount = models.CharField(db_column='GoodCount', max_length=50, blank=True, null=True)  # Field name made lowercase.
    generalcount = models.CharField(db_column='GeneralCount', max_length=50, blank=True, null=True)  # Field name made lowercase.
    aftercount = models.CharField(db_column='AfterCount', max_length=50, blank=True, null=True)  # Field name made lowercase.
    poorcount = models.CharField(db_column='PoorCount', max_length=50, blank=True, null=True)  # Field name made lowercase.
    imgurl = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jdproduct'
        unique_together = (('number', 'url', 'field_id'),)


class Jdproducts(models.Model):
    number = models.AutoField(primary_key=True)
    taskid = models.IntegerField(blank=True, null=True)
    names = models.CharField(max_length=200)
    url = models.CharField(max_length=250)
    field_id = models.CharField(db_column='_id', max_length=200)  # Field renamed because it started with '_'.
    reallyprice = models.CharField(db_column='reallyPrice', max_length=50)  # Field name made lowercase.
    originalprice = models.CharField(db_column='originalPrice', max_length=50, blank=True, null=True)  # Field name made lowercase.
    favourabledesc1 = models.CharField(db_column='favourableDesc1', max_length=300, blank=True, null=True)  # Field name made lowercase.
    allcount = models.CharField(db_column='AllCount', max_length=50, blank=True, null=True)  # Field name made lowercase.
    goodcount = models.CharField(db_column='GoodCount', max_length=50, blank=True, null=True)  # Field name made lowercase.
    generalcount = models.CharField(db_column='GeneralCount', max_length=50, blank=True, null=True)  # Field name made lowercase.
    aftercount = models.CharField(db_column='AfterCount', max_length=50, blank=True, null=True)  # Field name made lowercase.
    poorcount = models.CharField(db_column='PoorCount', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'jdproducts'
        unique_together = (('number', 'url', 'field_id'),)


class MemUsage(models.Model):
    hostname = models.CharField(max_length=20)
    mem_total = models.CharField(max_length=20, blank=True, null=True)
    mem_free = models.CharField(max_length=20, blank=True, null=True)
    mem_use = models.CharField(max_length=20, blank=True, null=True)
    mem_usage = models.CharField(max_length=20, blank=True, null=True)
    check_time = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mem_usage'


class News(models.Model):
    number = models.AutoField(primary_key=True)
    taskid = models.IntegerField(blank=True, null=True)
    id = models.CharField(max_length=50)
    url = models.CharField(max_length=100)
    source = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    editor = models.CharField(max_length=100, blank=True, null=True)
    time = models.CharField(max_length=20, blank=True, null=True)
    content = models.CharField(max_length=5000, blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)
    phrases = models.CharField(max_length=255, blank=True, null=True)
    summary = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news'
        unique_together = (('number', 'id', 'url'),)


class Taobaoproduct(models.Model):
    number = models.AutoField(primary_key=True)
    taskid = models.IntegerField(blank=True, null=True)
    itemid = models.CharField(max_length=20)
    url = models.CharField(max_length=100)
    names = models.CharField(max_length=200, blank=True, null=True)
    price = models.CharField(max_length=20, blank=True, null=True)
    actualprice = models.CharField(max_length=255, blank=True, null=True)
    allcount = models.CharField(max_length=10, blank=True, null=True)
    goodcount = models.CharField(max_length=10, blank=True, null=True)
    aftercount = models.CharField(max_length=10, blank=True, null=True)
    generalcount = models.CharField(max_length=10, blank=True, null=True)
    poorcount = models.CharField(max_length=10, blank=True, null=True)
    sellerlink = models.CharField(max_length=100, blank=True, null=True)
    sellernick = models.CharField(db_column='sellerNick', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'taobaoproduct'
        unique_together = (('number', 'itemid', 'url'),)


class Task(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    depth = models.IntegerField(blank=True, null=True)
    process = models.IntegerField(blank=True, null=True)
    host = models.CharField(max_length=255, blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    mysql = models.CharField(max_length=255, blank=True, null=True)
    redis = models.CharField(max_length=255, blank=True, null=True)
    starttime = models.CharField(max_length=255, blank=True, null=True)
    runtime = models.CharField(max_length=255, blank=True, null=True)
    runtype = models.CharField(max_length=255, blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    jobid = models.CharField(max_length=255, blank=True, null=True)
    start_year = models.IntegerField(blank=True, null=True)
    start_month = models.IntegerField(blank=True, null=True)
    start_day = models.IntegerField(blank=True, null=True)
    end_year = models.IntegerField(blank=True, null=True)
    end_month = models.IntegerField(blank=True, null=True)
    end_day = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'task'


class Tbproduct(models.Model):
    number = models.AutoField(primary_key=True)
    itemid = models.CharField(max_length=20)
    url = models.CharField(max_length=100)
    names = models.CharField(max_length=200, blank=True, null=True)
    price = models.CharField(max_length=20, blank=True, null=True)
    actualprice = models.CharField(max_length=255, blank=True, null=True)
    allcount = models.CharField(max_length=10, blank=True, null=True)
    goodcount = models.CharField(max_length=10, blank=True, null=True)
    aftercount = models.CharField(max_length=10, blank=True, null=True)
    generalcount = models.CharField(max_length=10, blank=True, null=True)
    poorcount = models.CharField(max_length=10, blank=True, null=True)
    sellerlink = models.CharField(max_length=100, blank=True, null=True)
    sellernick = models.CharField(db_column='sellerNick', max_length=200, blank=True, null=True)  # Field name made lowercase.
    imgurl = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbproduct'
        unique_together = (('number', 'itemid', 'url'),)


class TimingTask(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    start_minutes = models.CharField(max_length=255, blank=True, null=True)
    end_minutes = models.CharField(max_length=255, blank=True, null=True)
    timing_number = models.IntegerField(blank=True, null=True)
    timing_type = models.CharField(max_length=255, blank=True, null=True)
    host = models.CharField(max_length=255, blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    mysql = models.CharField(max_length=255, blank=True, null=True)
    redis = models.CharField(max_length=255, blank=True, null=True)
    starttime = models.CharField(max_length=255, blank=True, null=True)
    runtype = models.CharField(max_length=255, blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    runnumber = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'timing_task'
