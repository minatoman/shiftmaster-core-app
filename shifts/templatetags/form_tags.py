from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    existing_classes = field.field.widget.attrs.get('class', '')
    new_class = f"{existing_classes} {css_class} mb-3".strip()
    field.field.widget.attrs['class'] = new_class
    return field

@register.filter(name='add_placeholder')
def add_placeholder(field, placeholder_text):
    field.field.widget.attrs['placeholder'] = placeholder_text
    return field
