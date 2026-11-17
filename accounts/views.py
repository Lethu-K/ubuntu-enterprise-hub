from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Service, Booking

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type') or 'customer'
        user = User.objects.create_user(username=username, password=password)
        Profile.objects.create(user=user, user_type=user_type)
        return redirect('/accounts/login/')
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.profile.user_type == 'entrepreneur':
                return redirect('/accounts/agent-dashboard/')
            else:
                return redirect('/accounts/client-dashboard/')
        else:
            return render(request, 'login.html', {'error': 'Wrong username or password'})
    return render(request, 'login.html')

@login_required
def client_dashboard(request):
    if request.user.profile.user_type != 'customer':
        return redirect('/accounts/agent-dashboard/')
    services = Service.objects.filter(is_active=True).order_by('-created_at')
    my_bookings = Booking.objects.filter(client=request.user).order_by('-created_at')
    return render(request, 'client_dashboard.html', {'services': services, 'my_bookings': my_bookings})

@login_required
def agent_dashboard(request):
    if request.user.profile.user_type != 'entrepreneur':
        return redirect('/accounts/client-dashboard/')
    my_services = Service.objects.filter(agent=request.user)
    job_requests = Booking.objects.filter(agent=request.user, status='pending').order_by('-created_at')
    my_jobs = Booking.objects.filter(agent=request.user, status='accepted')
    total_earnings = sum(b.service.price for b in Booking.objects.filter(agent=request.user, status='completed'))
    return render(request, 'agent_dashboard.html', {
        'my_services': my_services,
        'job_requests': job_requests,
        'my_jobs': my_jobs,
        'total_earnings': total_earnings,
    })

@login_required
def add_service(request):
    if request.user.profile.user_type != 'entrepreneur':
        return redirect('/accounts/client-dashboard/')
    if request.method == 'POST':
        Service.objects.create(
            agent=request.user,
            title=request.POST.get('title'),
            category=request.POST.get('category'),
            price=int(request.POST.get('price') or 0),
            description=request.POST.get('description'),
        )
        return redirect('/accounts/agent-dashboard/')
    return render(request, 'add_service.html')

@login_required
def book_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        Booking.objects.create(
            client=request.user,
            agent=service.agent,
            service=service,
            message=request.POST.get('message'),
        )
        return redirect('/accounts/client-dashboard/')
    return render(request, 'book_service.html', {'service': service})

@login_required
def update_booking(request, booking_id, action):
    booking = get_object_or_404(Booking, id=booking_id, agent=request.user)
    if action == 'accept':
        booking.status = 'accepted'
    elif action == 'decline':
        booking.status = 'declined'
    elif action == 'complete':
        booking.status = 'completed'
    booking.save()
    return redirect('/accounts/agent-dashboard/')

def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')