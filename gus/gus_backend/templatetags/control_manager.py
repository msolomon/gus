from django import template
from django.template import Node, NodeList, Template, Context, Variable
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag
def control(usr,group,label,url,permstring,props=None):
    #return "nyuk"
    a1=''
    if props:a1=["%s=\"%s\""%(i,x) for i,x in enumerate(props)]
    #return a1
    propstr=" ".join(a1)
    
    if usr.has_group_perm(group,permstring) or not permstring:
        return mark_safe("[<a href=\"%s\" %s \>%s</a>] "%(url,propstr,label))
    return ' no perms %s,%s'%(usr,group)

control.is_safe = True
@register.simple_tag
def has_group_perm(usr,group,permstring):
    
    if usr.has_group_perm(group,permstring) or not permstring:
        return True
    return False

