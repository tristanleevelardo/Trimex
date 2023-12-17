import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import thirdYear
from typing import Optional

class YourConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        student_name = self.scope['url_route']['kwargs']['student_name']
        await self.channel_layer.group_add(f"student_{student_name}", self.channel_name)
        print("connected")

    async def disconnect(self, close_code):
        print("WebSocket connection closed.")

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        print("WebSocket message received and echoed:", message)

        await self.send(text_data=json.dumps({"message": message}))

    @database_sync_to_async
    def get_latest_grade_sync(self, student_name: str) -> Optional[int]:
        try:
            # Assuming 'student_fullName' is the field that relates to the student in your model
            third_year = thirdYear.objects.filter(student_fullName=student_name).latest('modified_at')
            return third_year.grade
        except thirdYear.DoesNotExist:
            return None

    async def notify_grade_change(self, event):
        student_name = event['student_name']
        new_grade = event['new_grade']
        print(f"Received grade change notification for {student_name} with new grade: {new_grade}")

        latest_grade = await self.get_latest_grade_sync(student_name)  # Fixed method name
        if latest_grade is not None:
            notification_message = f"New grade ({new_grade}) available for {student_name}!"
            await self.send(text_data=json.dumps({"message": notification_message}))
            print("Notification message sent to the WebSocket client.")
