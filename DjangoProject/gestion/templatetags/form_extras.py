from django import template

register = template.Library()


#que es esto pues con esto funciona el filtro add_class
@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={'class': css})
