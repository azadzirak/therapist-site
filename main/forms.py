from django import forms
from .models import Appointment, TimeSlot
from django.db.models import Q

class AppointmentForm(forms.ModelForm):

    class Meta:

        model = Appointment
        fields = ["name", "email", "phone", "slot", "message"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500",
                "placeholder": "Your full name",
            }),

            "email": forms.EmailInput(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500",
                "placeholder": "you@example.com",
            }),

            "phone": forms.TextInput(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500",
                "placeholder": "+1 234 567 890",
            }),

            "slot": forms.Select(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500",
            }),

            "message": forms.Textarea(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500",
                "rows": 5,
                "placeholder": "Tell me briefly about your situation...",
            }),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.slot_is_unavailable = False 

        slots = TimeSlot.objects.filter(is_available=True)
        if self.is_bound:
            selected_slot_id = self.data.get("slot")
            if selected_slot_id:
                slots = TimeSlot.objects.filter(
                    Q(is_available=True) | Q(pk=selected_slot_id)
                )

        self.fields["slot"].queryset = (
            slots.order_by("date", "start_time")
        )

    def clean_slot(self):
        slot = self.cleaned_data.get("slot")
        if not slot: 
            return slot 
        if not slot.is_available: 
            self.slot_is_unavailable = True 
            raise forms.ValidationError(
                "This session is no longer available."
            )
        active_appointment_exists = Appointment.objects.filter(
            slot=slot,
            status__in=["pending", "confirmed"],
        ).exists()

        if active_appointment_exists:
            self.slot_is_unavailable = True 
            raise forms.ValidationError(
                "This session has already been booked."
            )
        return slot

    