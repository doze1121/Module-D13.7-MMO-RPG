from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from newsboard.models import Comment


@receiver(post_save, sender=Comment)
def send_mail(sender, instance, created, **kwargs):

    if created:
        user = instance.post.author

        html = render_to_string(
            'newsboard/messages/new_comment.html',
            {
                'user': user,
                'comment': instance,
             },
        )

        msg = EmailMultiAlternatives(
                subject=f'Вы получили новый отклик!',
                from_email='doze1121@yandex.ru',
                to=[user.email]
            )

        msg.attach_alternative(html, 'text/html')
        msg.send()
    else:
        user = instance.author

        html = render_to_string(
            'newsboard/messages/update_comment.html',
            {
                'user': user,
                'comment': instance,
             },
        )

        msg = EmailMultiAlternatives(
                subject=f'Обновлен статус вашего отклика!',
                from_email='doze1121@yandex.ru',
                to=[user.email]
            )

        msg.attach_alternative(html, 'text/html')
        msg.send()
