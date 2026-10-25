"""
Definition of admin for Autoparts.
"""

from django.contrib import admin
from .models import Blog, Comment, Feedback

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted', 'id')
    list_display_links = ('title',)
    search_fields = ('title', 'description', 'content')
    list_filter = ('posted',)
    date_hierarchy = 'posted'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'date')
    list_filter = ('date', 'post')
    search_fields = ('text',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('name', 'email', 'suggestions')
    readonly_fields = ('created_at',)