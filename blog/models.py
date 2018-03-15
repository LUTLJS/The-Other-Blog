from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags


class Category(models.Model):
    #Category needs a name.
    name = models.CharField(max_length=100)
    def __str__(self):
    	return self.name


class Tag(models.Model):
    #Tag needs a name too.
    name = models.CharField(max_length=100)
    def __str__(self):
    	return self.name


class Post(models.Model):
    """
    Post needs titile,body,created_time,modified_time,excerpt.And a ForeignKey is needed because a post could be belonged to many catogories.
    A ManyToManyField exists because the relationship between Post and Tag is many-to-many.
    """
    title = models.CharField(max_length=70)
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    excerpt = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category,on_delete=False)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User,on_delete=False)
    views = models.PositiveIntegerField(default=0)
    def __str__(self):
    	return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    class Meta:
        """docstring for Meta"""
        ordering = ['-created_time']

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):    
        # 如果没有填写摘要
        if not self.excerpt:
            # 首先实例化一个 Markdown 类，用于渲染 body 的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        # 调用父类的 save 方法将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)


            
