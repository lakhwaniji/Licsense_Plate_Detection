from django.urls import path
from . import views

urlpatterns = [
    path('detection/', views.detection, name="detection"),
    path('capture_image/', views.capture_image, name="capture_image"),
    path('visitor_vehicle/', views.visitor_vehicle, name="visitor_vehicle"),
    path('opening_gate/',views.opening_gate,name="opening_gate"),
    path('',views.index,name="index")
]
