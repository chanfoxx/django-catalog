from django import template


register = template.Library()


@register.filter
def mediapath(image):
    """Возвращает местоположение media."""
    if image:
        return f"/media/{image}"

    return "#"
