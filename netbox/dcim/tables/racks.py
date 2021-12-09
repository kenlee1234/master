from re import VERBOSE
import django_tables2 as tables
from django_tables2.utils import Accessor

from dcim.models import Rack, RackReservation, RackRole
from tenancy.tables import TenantColumn
from utilities.tables import (
    BaseTable, ButtonsColumn, ChoiceFieldColumn, ColorColumn, ColoredLabelColumn, LinkedCountColumn, MarkdownColumn,
    TagColumn, ToggleColumn, UtilizationColumn,
)

__all__ = (
    'RackTable',
    'RackReservationTable',
    'RackRoleTable',
)


#
# Rack roles
#

class RackRoleTable(BaseTable):
    pk = ToggleColumn()
    name = tables.Column(
        linkify=True,
        verbose_name='名称'
    )
    rack_count = tables.Column(
        verbose_name='机架列表'
    )
    color = ColorColumn(
        verbose_name='颜色'
    )
    description = tables.Column(
        verbose_name='描述'
    )
    actions = ButtonsColumn(RackRole)

    class Meta(BaseTable.Meta):
        model = RackRole
        fields = ('pk', 'name', 'rack_count', 'color', 'description', 'slug', 'actions')
        default_columns = ('pk', 'name', 'rack_count', 'color', 'description', 'actions')


#
# Racks
#

class RackTable(BaseTable):
    pk = ToggleColumn()
    name = tables.Column(
        order_by=('_name',),
        linkify=True,
        verbose_name='名称'
    )
    location = tables.Column(
        linkify=True,
        verbose_name='地点'
    )
    site = tables.Column(
        linkify=True,
        verbose_name='站点'
    )
    tenant = TenantColumn(
        verbose_name='租户'
    )
    status = ChoiceFieldColumn(
        verbose_name='状态'
    )
    facility_id = tables.Column(
        verbose_name='设施ID'
    )
    role = ColoredLabelColumn(
        verbose_name='角色'
    )
    u_height = tables.TemplateColumn(
        template_code="{{ record.u_height }}U",
        verbose_name='高度（机架单位）'
    )
    comments = MarkdownColumn()
    device_count = LinkedCountColumn(
        viewname='dcim:device_list',
        url_params={'rack_id': 'pk'},
        verbose_name='设备列表'
    )
    get_utilization = UtilizationColumn(
        orderable=False,
        verbose_name='空间'
    )
    get_power_utilization = UtilizationColumn(
        orderable=False,
        verbose_name='电力'
    )
    tags = TagColumn(
        url_name='dcim:rack_list'
    )

    class Meta(BaseTable.Meta):
        model = Rack
        fields = (
            'pk', 'name', 'site', 'location', 'status', 'facility_id', 'tenant', 'role', 'serial', 'asset_tag', 'type',
            'width', 'u_height', 'comments', 'device_count', 'get_utilization', 'get_power_utilization', 'tags',
        )
        default_columns = (
            'pk', 'name', 'site', 'location', 'status', 'facility_id', 'tenant', 'role', 'u_height', 'device_count',
            'get_utilization', 'get_power_utilization',
        )


#
# Rack reservations
#

class RackReservationTable(BaseTable):
    pk = ToggleColumn()
    reservation = tables.Column(
        accessor='pk',
        linkify=True,
        verbose_name='保留'
    )
    site = tables.Column(
        accessor=Accessor('rack__site'),
        linkify=True,
        verbose_name='站点'
    )
    tenant = TenantColumn(
        verbose_name='租户'
    )
    rack = tables.Column(
        linkify=True,
        verbose_name='机架'
    )
    unit_list = tables.Column(
        orderable=False,
        verbose_name='单元列表'
    )
    user = tables.Column(
        verbose_name='用户'
    )
    description = tables.Column(
        verbose_name='描述'
    )
    tags = TagColumn(
        url_name='dcim:rackreservation_list'
    )
    actions = ButtonsColumn(RackReservation)

    class Meta(BaseTable.Meta):
        model = RackReservation
        fields = (
            'pk', 'reservation', 'site', 'rack', 'unit_list', 'user', 'created', 'tenant', 'description', 'tags',
            'actions',
        )
        default_columns = (
            'pk', 'reservation', 'site', 'rack', 'unit_list', 'user', 'description', 'actions',
        )
