from django import template

register = template.Library()


@register.simple_tag
def can_delete(recipient, user):
    """Return ``XxxRecipient.can_delete``
    """
    return recipient.can_delete(user)
