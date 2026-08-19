from django.db import models


class Appointment(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    slot = models.ForeignKey(
        "TimeSlot", 
        on_delete=models.PROTECT,
        related_name="appointments",
    )
    
    message = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending",)

    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.name} - {self.slot}"
    

class TimeSlot(models.Model):

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.date.strftime('%A, %B %d')} | {self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}"

class Service(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    