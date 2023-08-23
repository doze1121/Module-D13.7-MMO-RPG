from django.template import Library

register = Library()


@register.simple_tag()
def get_items_for_main_menu(request):
    is_authenticated = request.user.is_authenticated
    ITEMS = [
        {'title': 'Новости', 'url_name': 'newsboard:home'}
    ]

    if is_authenticated:
        ITEMS.append({'title': 'Мои отклики', 'url_name': 'newsboard:my_comments'})
        ITEMS.append({'title': 'Добавить новость', 'url_name': 'newsboard:create'})

    return ITEMS
