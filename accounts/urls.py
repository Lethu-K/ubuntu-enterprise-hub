from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('client-dashboard/', views.client_dashboard, name='client_dashboard'),
    path('agent-dashboard/', views.agent_dashboard, name='agent_dashboard'),
    path('add-service/', views.add_service, name='add_service'),
    path('book/<int:service_id>/', views.book_service, name='book_service'),
    path('booking/<int:booking_id>/<str:action>/', views.update_booking, name='update_booking'),
]