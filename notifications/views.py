from django.shortcuts import render,redirect, get_object_or_404
from django.http.response import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from notifications.models import Notification

@login_required
def notifications_list(request):
    user_notifications = request.user.notifications.all()
    return render(request,'notifications/notifications.html',{'notifications':user_notifications})

@login_required
def delete_notification(request,notification_id):
    notification = get_object_or_404(Notification,id=notification_id)
    if request.user == notification.receiver:
        if request.method=='POST':
            notification.delete()
        return redirect('notifications:list')
    return HttpResponseForbidden()