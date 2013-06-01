from django.contrib import admin

from reeder.feeds.models import Group, Feed, Item


class FeedAdmin(admin.ModelAdmin):
    list_display = ['title', 'group']


class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'feed', 'created_on_time']


admin.site.register(Group)
admin.site.register(Feed, FeedAdmin)
admin.site.register(Item, ItemAdmin)
