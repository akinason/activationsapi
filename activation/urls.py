from django.urls import path, include

from rest_framework.urlpatterns import format_suffix_patterns
from activation import views

app_name = 'activation'
urlpatterns = [
    path('softwares', views.SoftwareListView.as_view(), name="software_list"),
    path('softwares/<int:pk>', views.SoftwareDetailView.as_view()),
    path('orders', views.OrderListView.as_view()),
    path('orders/<int:pk>', views.OrderDetailView.as_view()),
    path('orders/email/resend', views.ResendEmailView.as_view()),

    path('merchant/', include('activation.public.urls'))

]

urlpatterns = format_suffix_patterns(urlpatterns)
