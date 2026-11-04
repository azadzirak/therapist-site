import jdatetime
from django import template

register = template.Library()

def convert_to_jalali(value):
    if not value:
        return None

    jalali_date = jdatetime.date.fromgregorian(date=value)

    return jalali_date.aslocale(jdatetime.FA_LOCALE)

@register.filter
def jalali_weekday(value):
    date = convert_to_jalali(value)

    if date is None:
        return ""

    return date.strftime("%A")

@register.filter
def jalali_date(value):
    date = convert_to_jalali(value)

    if date is None:
        return ""

    formatted_date = date.strftime("%d %B %Y")

    return formatted_date.translate(
        str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
    )

@register.filter
def persian_digits(value):
    if value is None:
        return ""

    return str(value).translate(
        str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
    )
