from django import template
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html

register = template.Library()

@register.filter
def render_notification_text(notification):
    notification_text=""
    if notification.type == "ARTICLE_PUBLISHED_FOR_AUTHOR":
        article = notification.content_object
        notification_text = format_html("Your {} has been successfully published.",render_article_link(article))
    elif notification.type == "ARTICLE_PUBLISHED_FOR_FOLLOWERS":
        article = notification.content_object
        author = None
        if article:
            author = article.author
        notification_text=format_html("User {} published a new {}.",render_user_badge(author),render_article_link(article))
    elif notification.type == "ARTICLE_LIKED":
        user = notification.content_object
        notification_text=format_html("User {} liked your article.",render_user_badge(user))
    elif notification.type == "COMMENT_CREATED":
        user = notification.content_object
        notification_text = format_html("User {} commented on your article.",render_user_badge(user))
    elif notification.type == "COMMENT_CREATED_FOR_PARENT":
        user = notification.content_object
        notification_text = format_html("User {} replied to your comment.",render_user_badge(user))
    elif notification.type == "COMMENT_LIKED":
        user = notification.content_object
        notification_text = format_html("User {} liked your comment.",render_user_badge(user))
    elif notification.type == "PROFILE_FOLLOW":
        user = notification.content_object
        notification_text = format_html("User {} has followed you",render_user_badge(user))
    return notification_text

@register.inclusion_tag('users/uncludes/user_badge.html')
def render_user_badge(user):
    if user:
        return render_to_string("users/includes/user_badge.html",{"account":user})
    return "[Deleted User]"

def render_article_link(article):
    if article:
        article_url = reverse('articles:detail',args=[article.id])
        return format_html("<a href='{}'>article</a>",article_url)
    return "[Deleted Article]"