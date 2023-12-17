# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import thirdYear

@receiver(post_save, sender=thirdYear)
def grade_change_handler(sender, instance, **kwargs):
    print("Grade change signal triggered!")
    channel_layer = get_channel_layer()
    student_name = instance.student_fullName  # Update this according to your model field
    new_grade = instance.finals  # Assuming 'finals' is the field you want to track
    print(student_name)
    print(new_grade)
    async_to_sync(channel_layer.group_send)(
        f"student_{student_name}",
        {
            'type': 'notify.grade_change',
            'student_name': student_name,
            'new_grade': new_grade,
        }
    )
    print("done")
