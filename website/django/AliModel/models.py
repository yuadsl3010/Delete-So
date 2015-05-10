from django.db import models

# Create your models here.
class db_status(models.Model):   
    name = models.CharField(primary_key=True, max_length=20)   
    status = models.DateTimeField(max_length=50)
    
    class Meta:     
        db_table = 'status' 

class db_commentdb(models.Model):
    cid = models.IntegerField(primary_key=True)
    userName = models.CharField(max_length=50)
    postDate = models.DateTimeField(max_length=50)
    sortDate = models.DateTimeField(max_length=50)
    contents = models.CharField(max_length=10000)
    
    class Meta:     
        db_table = 'commentdb' 
    
class db_comment2db(models.Model):
    id = models.IntegerField(primary_key=True)
    cid = models.IntegerField()
    userName = models.CharField(max_length=50)
    postDate = models.DateTimeField(max_length=50)
    contents = models.CharField(max_length=10000)
    
    class Meta:     
        db_table = 'comment2db' 