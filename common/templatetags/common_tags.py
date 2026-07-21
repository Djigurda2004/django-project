from datetime import timedelta
from django.utils import timezone
from django import template
from articles.models import Article
from comments.models import Comment

register = template.Library()

@register.filter
def render_creation_time(obj):
    time_now = timezone.now()
    time_since_creation = time_now-obj.created_at
    if isinstance(obj,Article) or isinstance(obj,Comment):
        time_since_update = time_now-obj.updated_at
        time_difference = time_since_creation-time_since_update
        if time_difference<timedelta(seconds=1):
            return f"Published {round_time(time_since_creation)} ago"
        else:
            return f"Published {round_time(time_since_creation)} ago (Updated {round_time(time_since_update)} ago)"
    else:
        return f"{round_time(time_since_creation)} ago"

def round_time(time):
    total_seconds = int(time.total_seconds())
    if total_seconds<60:
        return f"{total_seconds} second" if total_seconds==1 else f"{total_seconds} seconds"
    elif total_seconds<3600:
        total_minutes = total_seconds//60
        return f"{total_minutes} minute" if total_minutes==1 else f"{total_minutes} minutes"
    elif total_seconds<86400:
        total_hours = total_seconds//3600
        return f"{total_hours} hour" if total_hours==1 else f"{total_hours} hours"
    elif total_seconds<604800:
        total_days = total_seconds//86400
        return f"{total_days} day" if total_days==1 else f"{total_days} days"
    elif total_seconds<2592000:
        total_weeks = total_seconds//604800
        return f"{total_weeks} week" if total_weeks==1 else f"{total_weeks} weeks"
    elif total_seconds<31536000:
        total_months = total_seconds//2592000
        return f"{total_months} month" if total_months==1 else f"{total_months} months"
    else:
        total_years = total_seconds//31536000
        return f"{total_years} year" if total_years==1 else f"{total_years} years"