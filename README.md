# مشروع Django مع تكامل Kafka

هذا المشروع هو تطبيق ويب Django يتكامل مع Apache Kafka لإدارة الرسائل غير المتزامنة. يتم استخدام Docker و Docker Compose لتسهيل عملية الإعداد والتشغيل.

## المتطلبات الأساسية

*   [Docker](https://docs.docker.com/get-docker/)
*   [Docker Compose](https://docs.docker.com/compose/install/)

## الإعداد والتشغيل

1.  **استنساخ المستودع (إذا لم يكن موجودًا بالفعل):**
    ```bash
    git clone <repository-url>
    cd kafka_project
    ```

2.  **بناء وتشغيل الحاويات باستخدام Docker Compose:**
    ```bash
    docker-compose up --build -d
    ```
    سيقوم هذا الأمر ببناء الصور وتشغيل الخدمات المحددة في ملف `docker-compose.yml` (مثل تطبيق Django، Kafka، Zookeeper، وأي خدمات أخرى).

3.  **تطبيق تهجيرات قاعدة البيانات (Django Migrations):**
    قد تحتاج إلى تشغيل أوامر Django داخل حاوية الويب. أولاً، ابحث عن معرف حاوية خدمة الويب:
    ```bash
    docker-compose ps
    ```
    ثم قم بتشغيل التهجيرات:
    ```bash
    docker-compose exec <web_service_container_id_or_name> python manage.py migrate
    ```
    (استبدل `<web_service_container_id_or_name>` بالاسم أو المعرف الفعلي لحاوية خدمة الويب، غالبًا ما يكون شيئًا مثل `kafka_project_web_1`).

4.  **الوصول إلى التطبيق:**
    بمجرد تشغيل الحاويات وتطبيق التهجيرات، يجب أن يكون تطبيق Django متاحًا على `http://localhost:8000` (أو المنفذ المحدد في `docker-compose.yml`).

## إيقاف التطبيق

لإيقاف الحاويات:
```bash
docker-compose down
```

## هيكل المشروع

```
.
├── docker-compose.yml        # تعريف خدمات Docker Compose
├── manage.py                 # أداة إدارة Django
├── README.md                 # هذا الملف
├── grafana-provisioning/     # إعدادات Grafana (إذا كانت مستخدمة)
├── kafka_app/                # تطبيق Django الرئيسي
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── kafka_producer.py     # منطق منتج Kafka
│   ├── models.py             # نماذج Django
│   ├── tests.py
│   ├── urls.py               # روابط URL الخاصة بالتطبيق
│   ├── views.py              # عروض Django
│   └── migrations/           # تهجيرات قاعدة البيانات
├── kafka_project/            # إعدادات مشروع Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py           # إعدادات المشروع
│   ├── urls.py               # روابط URL الرئيسية للمشروع
│   └── wsgi.py
├── kafka2-data/              # بيانات Kafka (يتم إنشاؤها بواسطة Docker)
├── kafka3-data/              # بيانات Kafka (يتم إنشاؤها بواسطة Docker)
└── db.sqlite3                # قاعدة بيانات SQLite (للتطوير المحلي)
```

## التقنيات المستخدمة

*   **Backend:** Django (Python)
*   **Messaging:** Apache Kafka
*   **Containerization:** Docker, Docker Compose
*   **Database:** SQLite (افتراضي للتطوير، يمكن تغييره في `settings.py`)
*   **(اختياري) Monitoring:** Grafana, Prometheus (إذا تم تكوينهما)
