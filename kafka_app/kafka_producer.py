from confluent_kafka import Producer
import socket

# إعداد الاتصال مع Kafka Cluster (كل الـ brokers)
conf = {
    'bootstrap.servers': 'localhost:9094,localhost:9095,localhost:9096',  # تحديد الثلاثة Brokers
    'client.id': socket.gethostname(),
    'enable.idempotence': True,  # لضمان إرسال الرسائل مرة واحدة فقط
    'acks': 'all',  # تأكيد من جميع الـ Brokers، لضمان أن الرسالة تم تلقيها من الجميع
}

producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print(f"❌ Delivery failed: {err}")
    else:
        print(f"✅ Message delivered to {msg.topic()} [{msg.partition()}]")

def send_message_to_kafka(topic: str, message: str):
    try:
        producer.produce(topic, value=message.encode('utf-8'), callback=delivery_report)
        # تأجيل الـ flush قليلاً
        producer.poll(1)  # أو قم بإعطاء المنتج بعض الوقت لمعالجة الرسائل
         # الآن تأكد من أن جميع الرسائل تم إرسالها
    except Exception as e:
        print(f"⚠️ Error producing message: {e}") 
