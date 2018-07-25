from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# django的ORM
class Category(models.Model):

    name = models.CharField(max_length=100)
    category_ph = models.ImageField(u'类目图', upload_to='uploadImages')
    describes = models.CharField(max_length=100)

    # 相当于java中的tostring
    def __str__(self):
        return self.name

    # 列表缩略图展示需要加上此方法，另外需要在admin.py中绑定下admin_tagph,而不是tag_ph（tag_ph里面只是个地址）
    def admin_catph(self):
        return '<img src="/static/%s" height="50" width="50">' %(self.category_ph)
    admin_catph.allow_tags = True
    admin_catph.short_description = 'PIC'


class Tag(models.Model):

    name = models.CharField(max_length=100)
    tag_ph = models.ImageField(u'标签图', upload_to='uploadImages')
    describes = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    # 列表缩略图展示需要加上此方法，另外需要在admin.py中绑定下admin_tagph,而不是tag_ph（tag_ph里面只是个地址）
    def admin_tagph(self):
        return '<img src="/static/%s" height="50" width="50">' %(self.tag_ph)
    admin_tagph.allow_tags = True
    admin_tagph.short_description = 'PIC'


class Post(models.Model):

    title = models.CharField(max_length=70)
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    excerpt = models.CharField(max_length=200, blank=True)
    ph = models.ImageField(u'图片', upload_to='uploadImages')
    views = models.PositiveIntegerField(default=0)
    loves = models.PositiveIntegerField(default=0)
    life = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User)

    def __str__(self):
        return self.title

    # reverse 函数去解析视图函数对应的URL
    # 前端调用方式：{{ post.get_absolute_url }}: 这里把self.pk,即文章id传递给urls.py
    # 然后根据url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail')这个模式去解析出对应的/post/x）
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    # 列表缩略图展示需要加上此方法，另外需要在admin.admin_ph,而不是ph（ph里面只是个地址）
    def admin_ph(self):
        return '<img src="/static/%s" height="50" width="50">' %(self.ph)
    admin_ph.allow_tags = True
    admin_ph.short_description = 'PIC'

    # 阅读量，自增
    # 注意这里使用了 update_fields 参数来告诉 Django 只更新数据库中 views 字段的值，以提高效率
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    # 增加点赞
    def increase_loves(self):
        self.loves += 1
        self.save(update_fields=['loves'])

# 点赞数量一个IP只能点赞一次
class Poll(models.Model):
    ip = models.CharField(max_length=100, null=True, blank=True)
    blog = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.blog


