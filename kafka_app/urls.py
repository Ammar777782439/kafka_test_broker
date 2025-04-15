from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('send-kafka-message/', views.send_kafka_message, name='send_kafka_message'),
    path('send-kafka-ssl-message/', views.send_kafka_ssl_message, name='send_kafka_ssl_message'),
]
