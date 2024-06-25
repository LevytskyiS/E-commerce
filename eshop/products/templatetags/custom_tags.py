from django import template

register = template.Library()


@register.filter
def filter_by_name(queryset, name):
    return queryset.filter(attribute_name__name=name)
