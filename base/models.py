from django.db import models
from django.contrib.auth.models import User

class Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.name}"

class ImageUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True)  # Associate with a car
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(
        max_length=20,
        choices=[('manual', 'Manual'), ('face_recognition', 'Face Recognition')],
        default='manual'
    )

    def __str__(self):
        return f"{self.user.username} - {self.source} - {self.car.name if self.car else 'No Car'}"
