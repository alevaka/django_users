from django import template
from django.contrib.auth import get_user_model

User = get_user_model()
register = template.Library()


@register.simple_tag
def get_user_url():
    """
    Возвращает uuid пользователя для генерации ссылки на странице index.html
    """
    user0 = User.objects.first()
    if user0:
        return user0.id
    return ""
