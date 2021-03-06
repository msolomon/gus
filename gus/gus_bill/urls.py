
from django.conf.urls.defaults import *

urlpatterns = patterns('gus.gus_bill.views',
    (r'^$', 'index'),
    (r'^([0-9]+)/$', 'group_view'),
    (r'^Add/$', 'AddBill'),
    (r'^Add/(?P<group_id>[0-9]+)/$', 'AddBill'),
    (r'^Delete/(?P<bill_id>[0-9]+)/$', 'DeleteBill'),
    (r'^Payments/(?P<bill_id>[0-9]+)/$', 'Payments'),
    (r'^Archive/(?P<bill_id>[0-9]+)/$', 'Archive'),
)

