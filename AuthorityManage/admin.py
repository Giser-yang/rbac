from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission, ContentType
from AuthorityManage.models import Users, ImgList, FileManage, APIManage

admin.site.site_header = "后台系统"
admin.site.site_title = "权限管理"
# @admin.register(Users)

admin.site.register(Users, UserAdmin)
admin.site.register(Permission)
admin.site.register(ContentType)


# class FileManageAdmin(admin.ModelAdmin):
#     list_display = ('filetype', 'name', 'path', 'update_datetime')
#
#
# admin.site.register(FileManage, FileManageAdmin)
admin.site.register(FileManage)
admin.site.register(APIManage)
# Register your models here.
