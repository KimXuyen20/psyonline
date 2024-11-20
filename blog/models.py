from django.db import models

# Create your models here.

class Blog(models.Model):
    blog_name = models.CharField(max_length=500, unique=True)
    slug = models.SlugField(max_length=500, unique=True)
    description = models.TextField(max_length=1000, blank=True)
    images = models.ImageField(upload_to='photos/blogs')
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.blog_name


