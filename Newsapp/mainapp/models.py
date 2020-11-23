from django.db import models
from django.contrib.auth.models import User # import premade user model

# Create your models here.

class Member(User): # Extending the django User model, as it already includes the fields email, name, password
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False)

    interest_tag = models.CharField(max_length=50, default="None")
    profile_picture = models.ImageField(upload_to='profile_pictures', height_field=None, width_field=None, max_length=None, null=True)

    def __str__(self):
        return self.username


class Article(models.Model):
    article_name = models.CharField(max_length=200)
    article_author = models.CharField(max_length=50)
    article_date = models.DateField(auto_now=False, auto_now_add=False)
    article_tag = models.CharField(max_length=50)
    article_contents = models.CharField(max_length=10000)

    def __str__(self):
        return self.article_name


