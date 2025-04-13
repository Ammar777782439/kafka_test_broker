from django.urls import path
from .views import send_kafka_message
urlpatterns = [
    path('send-kafka/', send_kafka_message, name='send_kafka_message'),
]