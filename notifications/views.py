from django.shortcuts import render, HttpResponse

# Create your views here.

def notification_list(request):
    # Placeholder: In real code, fetch notifications for the user
    notifications = []
    return render(request, 'notifications/notification_list.html', {'notifications': notifications})

def mark_as_read(request, notification_id):
    return HttpResponse('Mark As Read Placeholder')

def mark_all_as_read(request):
    return HttpResponse('Mark All As Read Placeholder')
