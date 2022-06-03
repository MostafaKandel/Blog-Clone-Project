from venv import create
from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    text=models.TextField()
    create_date =models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date=timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk}) 

        '''
        After Someone creates a post, the user need to be taken to the posts
        detailed view page('post_detail'),
        Detailed view always needs the primary key(pk) to display/identify the post
        'self.pk' represents return to the detailed view of same post after creating

        First of all, when it comes to web development you really want to avoid hard coding paths in your templates.
 The reason for this is that paths might change, and it will be a hassle to go through all your HTML and templates to find every single URL
 or path and update it manually. It makes your code much harder to maintain.

The solution to this is to define functions that return the URL instead. This is where get_absolute_url() comes into the picture.
        '''



    def approve_comments(self):
        return self.comments.filter(approved_comment=True) 
        '''
        Any one can comment on a post, but all of them not gonna get approved,
        This method filters out unapproved(approved_comment = False) comments from Comment class,
        So that only approved(approved_comment = True) comments save to the model 'Post'
        '''

    def __str__(self):
        return self.title         


class Comment(models.Model):
    post=models.ForeignKey('blog.Post',related_name='comments',on_delete=models.CASCADE)
    author=models.CharField(max_length=200)
    text=models.TextField()
    create_date=models.DateTimeField(default=timezone.now)
    approved_comment=models.BooleanField(default=False)

    def approve(self):
        self.approved_comment=True
        self.save()

    def get_absolute_url(self):
        return reverse('post_list')

        '''
          return to the list view(ie the homepage) after commenting on
         a post, the comments needs approval to display
        '''

    def __str__(self):
        return self.text        
