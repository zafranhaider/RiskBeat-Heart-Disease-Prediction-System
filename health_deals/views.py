from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Notification
from django.shortcuts import render, get_object_or_404
# Home View - Displays notifications
def home(request):
      notifications = Notification.objects.all().order_by('-id')  # Fetch latest notifications
      return render(request, 'home1.html', {'notifications': notifications})
  
def notification_detail(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    return render(request, 'view.html', {'notification': notification})

# Upload Notification View - Handles manual form submissions
def upload_notification(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if title and description:
            notification = Notification(title=title, description=description, image=image)
            notification.save()
            messages.success(request, "Notification uploaded successfully!")
            return redirect('upload_notification')
        else:
            messages.error(request, "Please fill in all required fields.")

    return render(request, 'upload1.html')
