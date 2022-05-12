from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    image = models.ImageField(upload_to='category/')
    descriptions = models.TextField()

    def __str__(self):
        return self.name
class Tag(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
class Blog(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    descriptions = models.TextField()
    image = models.ImageField(upload_to='blog/')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category =models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
     blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     text = models.TextField()
     created = models.DateTimeField(auto_now_add=True)

     def __str__(self):
         return self.text
