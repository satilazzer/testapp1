from django import template
from django.utils.html import format_html

from ..models import Menu, MenuItem

register = template.Library()


@register.simple_tag
def draw_menu(menu_name):
    try:
        menu = Menu.objects.get(name=menu_name)
        items = MenuItem.objects.filter(menu=menu).select_related('parent')
    except Menu.DoesNotExist:
        return ''

    def render_menu_item(item, current_url):
        children = items.filter(parent=item)
        is_active = current_url == item.get_url()
        is_parent_active = is_active or any(child.get_url() == current_url for child in children)

        html = f'<li class={"active" if is_active else ""}>'
        html += f'<a href="{item.get_url()}">{item.title}</a>'
        if children:
            html += '<ul>'
            for child in children:
                html += render_menu_item(child, current_url)
            html += '</ul>'
        html += '</li>'
        return html

    current_url = '/'
    html = '<ul>'
    top_level_items = items.filter(parent__isnull=True)
    for item in top_level_items:
        html += render_menu_item(item, current_url)
    html += '</ul>'
    return format_html(html)
