from django.urls import path
from activation.public import views

app_name = 'public'
urlpatterns = [
    path('orders/<str:reference>', views.OrderDetailView.as_view()),
]

