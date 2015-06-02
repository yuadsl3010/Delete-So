from django.db import connection, models, transaction

class ac_comments(models.Manager):
    def search(self, sql, *args):
        rows = []
        try:
            cursor = connection.cursor()
            cursor.execute(sql, args)
            fetchall = cursor.fetchall()
            
            for obj in fetchall:
                row = dict()
                row['cid'] = obj[0]
                row['content'] = obj[1]
                row['userName'] = obj[2]
                row['layer'] = obj[3]
                row['acid'] = obj[4]
                row['isDelete'] = obj[5]
                row['type'] = obj[9]
                row['title'] = obj[10]
                row['up'] = obj[11]
                row['postTime'] = obj[12]
                row['url'] = obj[13]
                rows.append(row)
        except Exception:
            pass
            
        return rows
    
class ds_comments(models.Manager):
    def new_comment(self, *args):
        sql = '''
        INSERT INTO commentdb_test(userName, contents, sortDate, postDate)
        VALUES (%s, %s, %s, %s)
        '''
        try:
            cursor = connection.cursor()
            cursor.execute(sql, args)
        except Exception:
            pass
            
        return 
    
    def add_comment(self, *args):
        sql1 = '''
        INSERT INTO comment2db_test(cid, userName, contents, postDate)
        VALUES (%s, %s, %s, %s)
        '''
        sql2 = '''
        UPDATE commentdb_test SET sortDate = %s
        WHERE cid = %s
        '''
        try:
            cursor = connection.cursor()
            cursor.execute(sql1, args)
            sid = transaction.savepoint()
            cursor.execute(sql2, (args[3], args[0]))
            transaction.savepoint_commit(sid)
        except Exception as e:
            transaction.savepoint_rollback(sid)
            pass
        
        return
    
# Create your models here.
class db_status(models.Model):   
    name = models.CharField(primary_key=True, max_length=20)   
    status = models.DateTimeField(max_length=50)
    score = models.IntegerField()
    
    def __unicode__(self):
        return self.name + ': ' + self.status.strftime("%Y-%m-%d %H:%M:%S")
    
    class Meta:     
        db_table = 'status' 

class db_commentdb(models.Model):
    cid = models.IntegerField(primary_key=True)
    userName = models.CharField(max_length=50)
    postDate = models.DateTimeField(max_length=50)
    sortDate = models.DateTimeField(max_length=50)
    contents = models.CharField(max_length=10000)
    
    class Meta:     
        db_table = 'commentdb_test' 
    
class db_comment2db(models.Model):
    id = models.IntegerField(primary_key=True)
    cid = models.IntegerField()
    userName = models.CharField(max_length=50)
    postDate = models.DateTimeField(max_length=50)
    contents = models.CharField(max_length=10000)
    
    class Meta:     
        db_table = 'comment2db_test' 

class db_ac_contents_info(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=10)
    title = models.CharField(max_length=1000)
    up = models.CharField(max_length=1000)
    postTime = models.DateTimeField(max_length=50)
    url = models.CharField(max_length=50)
    
    class Meta:     
        db_table = 'accommentsinfo' 
             
class db_ac_contents_delete(models.Model):
    cid = models.IntegerField(primary_key=True)
    content = models.CharField(max_length=100000)
    userName = models.CharField(max_length=50)
    layer = models.IntegerField()
    acid = models.IntegerField()
    isDelete = models.IntegerField()
    siji = models.IntegerField()
    checkTime = models.DateTimeField(max_length=50)
    
    class Meta:     
        db_table = 'accomments_delete' 
        
class db_ac_contents_siji(models.Model):
    cid = models.IntegerField(primary_key=True)
    content = models.CharField(max_length=100000)
    userName = models.CharField(max_length=50)
    layer = models.IntegerField()
    acid = models.IntegerField()
    isDelete = models.IntegerField()
    siji = models.IntegerField()
    checkTime = models.DateTimeField(max_length=50)
    
    class Meta:     
        db_table = 'accomments_siji' 
        
class db_ac_refresh(models.Model):
    id = models.IntegerField(primary_key=True)
    createTime = models.DateTimeField(max_length=50)
    status = models.IntegerField()
    
    def __unicode__(self):
        return str(self.id) + '(' + str(self.status) + '): ' + self.createTime.strftime("%Y-%m-%d %H:%M:%S")
    
    class Meta:     
        db_table = 'acrefresh' 