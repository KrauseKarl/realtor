from django.contrib import admin
from app_news.models import News, Tag
from django.contrib.admin.actions import delete_selected


class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created', 'is_published']
    search_fields = ['title']

    delete_selected.short_description = "Удалить новость"


class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'tag_name', 'slug']
    prepopulated_fields = {"slug": ("tag_name",)}


admin.site.register(News, NewsAdmin)
admin.site.register(Tag, TagAdmin)
