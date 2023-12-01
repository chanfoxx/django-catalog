from django import template


register = template.Library()


@register.filter
def mediapath(image):
    """Возвращает местоположение media."""
    if image:
        return f"/media/{image}"

    return "#"


@register.filter(name='has_group')
def has_group(user, group_name):
    """Проверяет вхождение пользователя в группу."""
    return user.groups.filter(name=group_name).exists()
