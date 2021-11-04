from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, GroupManager
from django.utils.translation import gettext_lazy as _

# Create your models here.
STATUS_CHOICES = (
    (0, "禁用"),
    (1, "启用"),
)


class ImgList(models.Model):
    id = models.AutoField(primary_key=True, help_text="Id", verbose_name="Id")
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name="名称", help_text="名称")
    url = models.ImageField(upload_to='imgs/%Y%m%d/', help_text="图片路径", verbose_name="图片路径")
    update_datetime = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="修改时间", verbose_name="修改时间")
    create_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间",
                                           verbose_name="创建时间")

    class Meta:
        db_table = 'system_img_list'
        verbose_name = '图片管理'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


class FileManage(models.Model):
    id = models.AutoField(primary_key=True, help_text="Id", verbose_name="Id")
    filetype = models.CharField(max_length=200, null=True, blank=True, verbose_name="文件类型", help_text="文件类型")
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name="名称", help_text="名称")
    path = models.CharField(max_length=200, null=True, blank=True, verbose_name="文件路径", help_text="文件路径")
    update_datetime = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="修改时间", verbose_name="修改时间")
    create_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间",
                                           verbose_name="创建时间")

    class Meta:
        db_table = 'system_file_manage'
        verbose_name = '文件权限管理'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


class APIManage(models.Model):
    id = models.AutoField(primary_key=True, help_text="Id", verbose_name="Id")
    APItype = models.CharField(max_length=200, null=True, blank=True, verbose_name="接口类型", help_text="接口类型")
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name="名称", help_text="名称")
    url = models.CharField(max_length=200, null=True, blank=True, verbose_name="路由地址", help_text="路由地址")
    update_datetime = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="修改时间", verbose_name="修改时间")
    create_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间",
                                           verbose_name="创建时间")

    class Meta:
        db_table = 'system_api_manage'
        verbose_name = 'API接口权限管理'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


class Users(AbstractUser):
    id = models.AutoField(primary_key=True, help_text="Id", verbose_name="Id")
    username = models.CharField(max_length=150, unique=True, db_index=True, verbose_name='用户账号', help_text="用户账号")
    email = models.EmailField(max_length=255, verbose_name="邮箱", null=True, blank=True, help_text="邮箱")
    mobile = models.CharField(max_length=255, verbose_name="电话", null=True, blank=True, help_text="电话")
    avatar = models.ImageField(upload_to='imgs/%Y%m%d/', verbose_name="头像", null=True, blank=True, help_text="头像")
    name = models.CharField(max_length=40, verbose_name="姓名", help_text="姓名")
    GENDER_CHOICES = (
        (0, "女"),
        (1, "男"),
    )
    gender = models.IntegerField(choices=GENDER_CHOICES, verbose_name="性别", null=True, blank=True, help_text="性别")
    update_datetime = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="修改时间", verbose_name="修改时间")
    create_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间",
                                           verbose_name="创建时间")
    APIToUser = models.ManyToManyField(APIManage, blank=True)
    FileToUser = models.ManyToManyField(FileManage, blank=True)

    class Meta:
        db_table = "system_users"
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
        ordering = ('create_datetime',)


class Groups(Group):
    # name = models.CharField(_('name'), max_length=150, unique=True)
    update_datetime = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="修改时间", verbose_name="修改时间")
    create_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间",
                                           verbose_name="创建时间")
    APIToGroups = models.ManyToManyField(APIManage, blank=True)
    FileToGroups = models.ManyToManyField(FileManage, blank=True)

    objects = GroupManager()

    class Meta:
        db_table = "system_groups"
        verbose_name = '分组表'
        verbose_name_plural = verbose_name
        ordering = ('create_datetime',)

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)


class OperationLog(models.Model):
    id = models.AutoField(primary_key=True, help_text="Id", verbose_name="Id")
    description = models.CharField(max_length=255, verbose_name="描述", null=True, blank=True, help_text="描述")
    update_datetime = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="修改时间", verbose_name="修改时间")
    create_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间",
                                           verbose_name="创建时间")
    request_modular = models.CharField(max_length=64, verbose_name="请求模块", null=True, blank=True, help_text="请求模块")
    request_path = models.CharField(max_length=400, verbose_name="请求地址", null=True, blank=True, help_text="请求地址")
    request_body = models.TextField(verbose_name="请求参数", null=True, blank=True, help_text="请求参数")
    request_method = models.CharField(max_length=8, verbose_name="请求方式", null=True, blank=True, help_text="请求方式")
    request_msg = models.TextField(verbose_name="操作说明", null=True, blank=True, help_text="操作说明")
    request_ip = models.CharField(max_length=32, verbose_name="请求ip地址", null=True, blank=True, help_text="请求ip地址")
    request_browser = models.CharField(max_length=64, verbose_name="请求浏览器", null=True, blank=True, help_text="请求浏览器")
    response_code = models.CharField(max_length=32, verbose_name="响应状态码", null=True, blank=True, help_text="响应状态码")
    request_os = models.CharField(max_length=64, verbose_name="操作系统", null=True, blank=True, help_text="操作系统")
    json_result = models.TextField(verbose_name="返回信息", null=True, blank=True, help_text="返回信息")
    status = models.BooleanField(default=False, verbose_name="响应状态", help_text="响应状态")

    class Meta:
        db_table = 'system_operation_log'
        verbose_name = '操作日志'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)
