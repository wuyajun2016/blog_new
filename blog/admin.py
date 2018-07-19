from django.contrib import admin
from .models import Post, Category, Tag


# 为后台添加自定义字段展示
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author', 'admin_ph']

    readonly_fields = ('admin_ph',)  # 必须加这行 否则访问编辑页面并不会展示缩略图

    # 编辑页面，展示缩略图需要加上此方法
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields
        return self.readonly_fields


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'describes', 'admin_catph']   # 注意：必须设置字段为list_dispaly
    ordering = ("id",)              # 列表按升序排

    readonly_fields = ('admin_catph',)  # 必须加这行 否则访问编辑页面并不会展示缩略图

    # 编辑页面，展示缩略图需要加上此方法
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields
        return self.readonly_fields


class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'describes', 'admin_tagph']

    readonly_fields = ('admin_tagph',)  # 必须加这行 否则访问编辑页面并不会展示缩略图

    # 编辑页面，展示缩略图需要加上此方法
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields
        return self.readonly_fields


# 注册我们新增加的模型，才能在后台展示
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
