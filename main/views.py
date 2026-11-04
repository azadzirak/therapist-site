from django.shortcuts import render
from .forms import AppointmentForm
from .models import Service, TimeSlot
from django.db import transaction
from django.utils.translation import gettext as _

def home(request):
    services = Service.objects.filter(is_active=True)
    language = request.LANGUAGE_CODE

    for service in services:
        if language == "fa":
            service.display_title = service.title_fa or service.title
            service.display_description = (
                service.description_fa or service.description
            )
        else: 
            service.display_title = service.title
            service.display_description = service.description
            
    return render(
        request,
        "main/home.html",
        {
            "services": services
        }
    )

def about(request):
    return render(request, "main/about.html")

def contact(request):
    return render(request, "main/contact.html")

def appointment(request):

    if request.method == "POST":
        form = AppointmentForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                slot = TimeSlot.objects.select_for_update().get(
                    pk=form.cleaned_data["slot"].pk
                )

                if not slot.is_available:
                    form.add_error(
                        "slot",
                        _("This session has just been booked.")
                    )
                else:
                    appointment = form.save(commit=False)
                    appointment.slot = slot
                    appointment.save()

                    slot.is_available = False
                    slot.save()

                    return render(
                        request,
                        "main/appointment_success.html",
                        {
                            "appointment": appointment
                        }
                    )

    else:
        form = AppointmentForm()

    return render(
        request,
        "main/appointment.html",
        {"form": form}
    )

