from django.db import models

class Comment(models.Model):

    comment_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(default=0, db_index=True)
    comment_page = models.URLField(default='', db_index=True)
    comment_type = models.SmallIntegerField(help_text='1: normal comment, 2: reply', default=1)
    comment_date = models.DateTimeField('date published')
    comment_content = models.TextField(max_length=4096)
    comment_ups = models.IntegerField(default=0)
    comment_downs = models.IntegerField(default=0)
    comment_parent = models.BigIntegerField(default=0)

