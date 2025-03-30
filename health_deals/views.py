from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Notification
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from .models import Subscriber

# Home View - Displays notifications
def home(request):
      notifications = Notification.objects.all().order_by('-id')  # Fetch latest notifications
      return render(request, 'home1.html', {'notifications': notifications})
  
def notification_detail(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    return render(request, 'view.html', {'notification': notification})




def is_superuser(user):
    return user.is_authenticated and user.is_superuser

def notify(request):
  return render(request, 'subscribe_form.html')

@csrf_exempt  # Only if necessary, otherwise use CSRF token in AJAX request
def subscribe_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if email:
            if not Subscriber.objects.filter(email=email).exists():
                Subscriber.objects.create(email=email)
                return JsonResponse({"message": "You have subscribed successfully!"})
            return JsonResponse({"message": "You are already subscribed!"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@user_passes_test(lambda u: u.is_superuser)
def upload_notification(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if title and description:
            notification = Notification(title=title, description=description, image=image)
            notification.save()

            # Send email to all subscribers
            subscribers = Subscriber.objects.values_list('email', flat=True)
            if subscribers:
                send_mail(
                    subject="New Deal Available",
                    message=f"{title}\n\n{description}",
                    from_email="admin@example.com",
                    recipient_list=list(subscribers),
                    fail_silently=False,
                )

            messages.success(request, "Notification uploaded successfully!")
            return redirect('upload_notification')
        else:
            messages.error(request, "Please fill in all required fields.")

    return render(request, 'upload1.html')


@csrf_exempt
def unsubscribe_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            if Subscriber.objects.filter(email=email).exists():
                Subscriber.objects.filter(email=email).delete()
                return JsonResponse({"message": "You have unsubscribed successfully!"})
            else:
                return JsonResponse({"message": "You are not subscribed!"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)


def check_subscription(request):
    email = request.GET.get("email")
    if email and Subscriber.objects.filter(email=email).exists():
        return JsonResponse({"subscribed": True})
    return JsonResponse({"subscribed": False})