from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from froala_editor.fields import FroalaField
from .helper import *
# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
    
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT ='DF', 'Draft'
        PUBLISHED ='PB','Published'
    title=models.CharField(max_length=250)
    slug=models.SlugField(max_length=1000,unique_for_date='publish',null=True,blank=True)
    # body=models.TextField()
    body=FroalaField()
    publish=models.DateField(default=timezone.now)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    image=models.ImageField(upload_to='blogImage',blank=True,null=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=2, choices=Status.choices,default=Status.DRAFT)
    objects=models.Manager()  #default manage
    published= PublishedManager() #custom manage
    tags=TaggableManager()
    class Meta:
        ordering=['-publish']
        indexes=[models.Index(fields=['-publish']),]
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('blog:post_detail',args=[self.publish.year,self.publish.month,self.publish.day,self.slug])
    
    def save(self,*args,**kwargs):
        self.slug=generate_slug(self.title)
        super(Post,self).save(*args,**kwargs)

class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email= models.CharField(max_length=500)
    body= models.TextField(default=None)
    created= models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now_add=True)
    active= models.BooleanField(default=True)

    class Meta:
        ordering=['created']
        indexes=[models.Index(fields=['created'])]
        def __str__(self):
            return f'Comment by {self.name} on {self.post}'
