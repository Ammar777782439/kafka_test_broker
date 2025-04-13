from django.http import JsonResponse
from .kafka_producer import send_message_to_kafka

def send_kafka_message(request):
    message = request.GET.get("msg", "Hello froتتتتتتDjango!")
    send_message_to_kafka("test-topic", message)
    return JsonResponse({"status": "sent", "message": message})
