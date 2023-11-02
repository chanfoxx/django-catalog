from django import template


register = template.Library()


@register.simple_tag
def mediapath(image):
    """Возвращает местоположение media."""
    if image:
        return f"/media/{image}"

    return "#"
