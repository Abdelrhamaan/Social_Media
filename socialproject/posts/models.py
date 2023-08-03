from django.db import models
from django.conf import settings
from django.utils.text import slugify
# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/%y/%m/%d')
    caption = models.TextField(blank=True)
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, blank=True)
    created = models.DateField(auto_now_add=True)
    liked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name='posts_liked')

    def __str__(self):
        return self.title

    '''
    Imagine if you have a personal blog with the URL http://mysite.com. In that blog you have a post with the title ‘A day in my life’.

    The URL to this post may look like the following:

    http://mysite.com/a-day-in-my-life '''

    def save(self, *args, **kargs):
        if not self.slug:
            # if there is no slug set it with title
            self.slug = slugify(self.title)
        super().save(*args, **kargs)


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, default=2)
    body = models.TextField(max_length=400)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.body
