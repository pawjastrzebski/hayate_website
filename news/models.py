from django.db import models
from users.models import User

class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date = models.DateField(auto_now=True)
    user_id = models.ForeignKey('users.User', on_delete=models.CASCADE)

    
    class Meta:
        db_table = 'news'