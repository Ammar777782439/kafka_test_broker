# مشروع Django مع تكامل Kafka SSL

هذا المشروع هو تطبيق ويب Django يتكامل مع Apache Kafka باستخدام SSL للاتصال الآمن. يتم استخدام Docker و Docker Compose لتسهيل عملية الإعداد والتشغيل.

## المتطلبات الأساسية

*   [Python 3.8+](https://www.python.org/downloads/)
*   [Docker](https://docs.docker.com/get-docker/)
*   [Docker Compose](https://docs.docker.com/compose/install/)
*   [OpenSSL](https://www.openssl.org/)
*   [Java/JDK](https://www.oracle.com/java/technologies/javase-downloads.html) (مطلوب لأدوات keytool)

## الإعداد والتشغيل

### 1. تثبيت المتطلبات

قم بتثبيت المتطلبات باستخدام pip:

```bash
pip install -r requirements.txt
```

### 2. إنشاء موضوع (Topic) في كافكا

بعد تشغيل كافكا باستخدام Docker Compose، قم بإنشاء موضوع للاختبار:

```bash
python create_kafka_topic.py test-topic
```

سيقوم هذا البرنامج النصي بإنشاء موضوع `test-topic` في كافكا.

### 3. تشغيل Kafka باستخدام Docker Compose

قم بتشغيل Kafka باستخدام Docker Compose:

```bash
docker-compose up -d
```

### 4. تشغيل تطبيق Django

قم بتطبيق ترحيلات قاعدة البيانات:

```bash
python manage.py migrate
```

ثم قم بتشغيل خادم التطوير:

```bash
python manage.py runserver
```

يمكنك الآن الوصول إلى التطبيق على `http://localhost:8000`.

## استخدام التطبيق

1. انتقل إلى الصفحة الرئيسية على `http://localhost:8000`
2. انقر على "فتح نموذج SSL" لفتح نموذج إرسال الرسائل باستخدام SSL
3. أدخل الموضوع (Topic) والرسالة التي تريد إرسالها
4. انقر على "إرسال الرسالة" لإرسال الرسالة إلى Kafka

## هيكل المشروع

```
.
├── docker-compose.yml        # تعريف خدمات Docker Compose
├── create_kafka_topic.py     # برنامج نصي لإنشاء موضوع في كافكا
├── manage.py                 # أداة إدارة Django
├── README.md                 # هذا الملف
├── requirements.txt          # متطلبات Python
├── kafka_app/                # تطبيق Django الرئيسي
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── kafka_producer.py     # منطق منتج Kafka مع دعم SSL
│   ├── models.py             # نماذج Django
│   ├── templates/            # قوالب HTML
│   │   └── kafka_app/
│   │       ├── home.html
│   │       └── send_ssl_message.html
│   ├── tests.py
│   ├── urls.py               # روابط URL الخاصة بالتطبيق
│   ├── views.py              # عروض Django
│   └── migrations/           # ترحيلات قاعدة البيانات
├── kafka_project/            # إعدادات مشروع Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py           # إعدادات المشروع
│   ├── urls.py               # روابط URL الرئيسية للمشروع
│   └── wsgi.py
└── db.sqlite3                # قاعدة بيانات SQLite (للتطوير المحلي)
```

## التقنيات المستخدمة

*   **Backend:** Django (Python)
*   **Messaging:** Apache Kafka with SSL
*   **Kafka Client:** confluent-kafka-python
*   **Containerization:** Docker, Docker Compose
*   **Security:** SSL/TLS for Kafka communication
*   **Database:** SQLite (افتراضي للتطوير، يمكن تغييره في `settings.py`)

## استكشاف الأخطاء وإصلاحها

### مشاكل الاتصال بـ SSL

إذا واجهت مشاكل في الاتصال بـ Kafka باستخدام SSL، تأكد من:

1. تم تشغيل حاوية Kafka بشكل صحيح باستخدام Docker Compose
2. منفذ SSL (9093) متاح ويمكن الوصول إليه
3. تم تعطيل التحقق من الشهادة في `kafka_producer.py` باستخدام `ssl.endpoint.identification.algorithm: 'none'`

### مشاكل الاتصال بـ Kafka

إذا لم يتمكن التطبيق من الاتصال بـ Kafka، تأكد من:

1. Kafka يعمل ويمكن الوصول إليه على المنفذ المحدد
2. إعدادات الاتصال في `kafka_producer.py` صحيحة
3. تم تكوين موضوعات Kafka بشكل صحيح
