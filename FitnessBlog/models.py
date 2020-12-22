from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Post(models.Model):
    post_title = models.CharField(max_length=50)
    post_content = models.TextField()
    post_date = models.DateTimeField(default=timezone.now)
    post_author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='blog_posts')  # Represents the like of the specific post

    def total_likes(self):
        return self.likes.count()  # Counts the total number of likes.

    def __str__(self):
        return self.post_title

    def get_absolute_url(self):
        return reverse ('post-detail', kwargs={'pk': self.pk})  # Returns the full path for a string Instance specific
