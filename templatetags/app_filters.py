from django import template

register = template.Library()

@register.filter(name='get_all_threads')
def get_all_threads( value ) :
    
    return value.threads.all()