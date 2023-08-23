from django.contrib import admin
from django.core.mail import send_mail

from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'date')

    def send_email(self, request, queryset):
        for contact in queryset:
            subject = 'Новое сообщение'
            message = 'Привет, у вас новое сообщение! т.к. вы недавно подписались на новостную рассылку'
            from_email = 'doze1121@yandex.ru'
            recipient_list = [contact.email]
            send_mail(subject, message, from_email, recipient_list)
        self.message_user(request, 'Сообщение успешно отправлено')

    send_email.short_description = 'Отправить сообщение'

    actions = [send_email]
