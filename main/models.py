from django.db import models
from django.utils.translation import gettext_lazy as _

class Appointment(models.Model):

    STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("confirmed", _("Confirmed")),
        ("cancelled", _("Cancelled")),
    ] 

    name = models.CharField(max_length=100, verbose_name=_("Name"))
    email = models.EmailField(verbose_name=_("Email"))
    phone = models.CharField(max_length=20, verbose_name=_("Phone Number"))

    slot = models.ForeignKey(
        "TimeSlot", 
        on_delete=models.PROTECT,
        related_name="appointments",
        verbose_name=_("Slot"),
    )
    
    message = models.TextField(blank=True, verbose_name=_("Message"))

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending",verbose_name=_("Status"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    

    def __str__(self):
        return f"{self.name} - {self.slot}"
    

class TimeSlot(models.Model):

    date = models.DateField(verbose_name=_("Date"))
    start_time = models.TimeField(verbose_name=_("Start Time"))
    end_time = models.TimeField(verbose_name=_("End Time"))
    is_available = models.BooleanField(default=True, verbose_name=_("Is Available"))

    def __str__(self):
        return f"{self.date.strftime('%A, %B %d')} | {self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}"

class Service(models.Model):

    title = models.CharField(max_length=100, verbose_name=_("Title"))
    title_fa = models.CharField(max_length=100, blank=True, default="", verbose_name=_("Persian Title"))
    description = models.TextField(verbose_name=_("Description"))
    description_fa = models.TextField(blank=True, default="", verbose_name=_("Persion Description"))
    icon = models.CharField(max_length=10, verbose_name=_("Icon"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    def __str__(self):
        return self.title
