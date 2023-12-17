from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/student/(?P<student_name>[\w\-]+)/$", consumers.YourConsumer.as_asgi()),
]
 