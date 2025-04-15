from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging

from .kafka_producer import get_kafka_ssl_producer

logger = logging.getLogger(__name__)

def home(request):
    """
    Render the home page with options to send messages to Kafka.
    """
    return render(request, 'kafka_app/home.html')

def send_kafka_message(request):
    """
    Send a message to Kafka using PLAINTEXT protocol.
    This is a simple example and not used with SSL.
    """
    message = request.GET.get('msg', 'Default message')
    topic = request.GET.get('topic', 'test-topic')

    # For demonstration, we'll just return a message that this isn't implemented
    # since we're focusing on SSL
    return HttpResponse(f"PLAINTEXT messaging not implemented. We're focusing on SSL. Message: {message}, Topic: {topic}")

def send_kafka_ssl_message_form(request):
    """
    Render the form for sending SSL messages to Kafka.
    """
    context = {}
    return render(request, 'kafka_app/send_ssl_message.html', context)

@csrf_exempt
def send_kafka_ssl_message(request):
    """
    Send a message to Kafka using SSL encryption.
    """
    if request.method == 'GET':
        return send_kafka_ssl_message_form(request)

    elif request.method == 'POST':
        try:
            # Get form data
            topic = request.POST.get('topic', 'test-topic')
            message = request.POST.get('message', 'Default message')

            # Get the Kafka producer with SSL
            producer = get_kafka_ssl_producer()

            # Send the message
            success = producer.send_message(topic, message)

            if success:
                result = f"Message sent successfully to topic '{topic}'"
                logger.info(result)
                return render(request, 'kafka_app/send_ssl_message.html', {
                    'result': result,
                    'success': True
                })
            else:
                result = f"Failed to send message to topic '{topic}'"
                logger.error(result)
                return render(request, 'kafka_app/send_ssl_message.html', {
                    'result': result,
                    'success': False
                })

        except Exception as e:
            error_msg = f"Error sending message to Kafka: {str(e)}"
            logger.exception(error_msg)
            return render(request, 'kafka_app/send_ssl_message.html', {
                'result': error_msg,
                'success': False
            })
