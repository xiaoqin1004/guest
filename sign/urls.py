from django.urls import path
from sign import views_if

urlpatterns = [
    path('add_event/', views_if.add_event),
    path('get_event_list/', views_if.get_event_list),
    # path('add_guest/', views_if.add_guest),
    # path('get_guest_list/', views_if.get_guest_list),
    # path('user_sign/', views_if.user_sign),
]