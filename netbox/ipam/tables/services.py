import django_tables2 as tables

from utilities.tables import BaseTable, TagColumn, ToggleColumn
from ipam.models import *

__all__ = (
    'ServiceTable',
)


#
# Services
#

class ServiceTable(BaseTable):
    pk = ToggleColumn()
    name = tables.Column(
        linkify=True,
        verbose_name='名称'
    )
    parent = tables.Column(
        linkify=True,
        order_by=('device', 'virtual_machine'),
        verbose_name='父设备'
    )
    protocol = tables.Column(
        verbose_name='协议'
    )
    ports = tables.TemplateColumn(
        template_code='{{ record.port_list }}',
        verbose_name='端口列表'
    )
    description = tables.Column(
        verbose_name='描述'
    )
    tags = TagColumn(
        url_name='ipam:service_list'
    )

    class Meta(BaseTable.Meta):
        model = Service
        fields = ('pk', 'name', 'parent', 'protocol', 'ports', 'ipaddresses', 'description', 'tags')
        default_columns = ('pk', 'name', 'parent', 'protocol', 'ports', 'description')
