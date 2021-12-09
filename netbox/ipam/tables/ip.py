import django_tables2 as tables
from django.utils.safestring import mark_safe
from django_tables2.utils import Accessor

from tenancy.tables import TenantColumn
from utilities.tables import (
    BaseTable, BooleanColumn, ButtonsColumn, ChoiceFieldColumn, LinkedCountColumn, TagColumn,
    ToggleColumn, UtilizationColumn,
)
from ipam.models import *

__all__ = (
    'AggregateTable',
    'InterfaceIPAddressTable',
    'IPAddressAssignTable',
    'IPAddressTable',
    'IPRangeTable',
    'PrefixTable',
    'RIRTable',
    'RoleTable',
)

AVAILABLE_LABEL = mark_safe('<span class="badge bg-success">Available</span>')

PREFIX_LINK = """
{% load helpers %}
{% if record.depth %}
    <div class="record-depth">
        {% for i in record.depth|as_range %}
            <span>•</span>
        {% endfor %}
    </div>
{% endif %}
<a href="{% if record.pk %}{% url 'ipam:prefix' pk=record.pk %}{% else %}{% url 'ipam:prefix_add' %}?prefix={{ record }}{% if object.vrf %}&vrf={{ object.vrf.pk }}{% endif %}{% if object.site %}&site={{ object.site.pk }}{% endif %}{% if object.tenant %}&tenant_group={{ object.tenant.group.pk }}&tenant={{ object.tenant.pk }}{% endif %}{% endif %}">{{ record.prefix }}</a>
"""

PREFIXFLAT_LINK = """
{% load helpers %}
{% if record.pk %}
    <a href="{% url 'ipam:prefix' pk=record.pk %}">{{ record.prefix }}</a>
{% else %}
    {{ record.prefix }}
{% endif %}
"""

IPADDRESS_LINK = """
{% if record.pk %}
    <a href="{{ record.get_absolute_url }}">{{ record.address }}</a>
{% elif perms.ipam.add_ipaddress %}
    <a href="{% url 'ipam:ipaddress_add' %}?address={{ record.1 }}{% if object.vrf %}&vrf={{ object.vrf.pk }}{% endif %}{% if object.tenant %}&tenant={{ object.tenant.pk }}{% endif %}" class="btn btn-sm btn-success">{% if record.0 <= 65536 %}{{ record.0 }}{% else %}Many{% endif %} IP{{ record.0|pluralize }} available</a>
{% else %}
    {% if record.0 <= 65536 %}{{ record.0 }}{% else %}Many{% endif %} IP{{ record.0|pluralize }} available
{% endif %}
"""

IPADDRESS_ASSIGN_LINK = """
<a href="{% url 'ipam:ipaddress_edit' pk=record.pk %}?{% if request.GET.interface %}interface={{ request.GET.interface }}{% elif request.GET.vminterface %}vminterface={{ request.GET.vminterface }}{% endif %}&return_url={{ request.GET.return_url }}">{{ record }}</a>
"""

VRF_LINK = """
{% if record.vrf %}
    <a href="{{ record.vrf.get_absolute_url }}">{{ record.vrf }}</a>
{% elif object.vrf %}
    <a href="{{ object.vrf.get_absolute_url }}">{{ object.vrf }}</a>
{% else %}
    Global
{% endif %}
"""


#
# RIRs
#

class RIRTable(BaseTable):
    pk = ToggleColumn()
    name = tables.Column(
        linkify=True,
        verbose_name='名称'
    )
    is_private = BooleanColumn(
        verbose_name='私有'
    )
    aggregate_count = LinkedCountColumn(
        viewname='ipam:aggregate_list',
        url_params={'rir_id': 'pk'},
        verbose_name='聚合列表'
    )
    description = tables.Column(
        verbose_name='描述'
    )
    actions = ButtonsColumn(RIR)

    class Meta(BaseTable.Meta):
        model = RIR
        fields = ('pk', 'name', 'slug', 'is_private', 'aggregate_count', 'description', 'actions')
        default_columns = ('pk', 'name', 'is_private', 'aggregate_count', 'description', 'actions')


#
# Aggregates
#

class AggregateTable(BaseTable):
    pk = ToggleColumn()
    rir = tables.Column(
        verbose_name='区域互联网注册管理机构'
    )
    prefix = tables.Column(
        linkify=True,
        verbose_name='聚合'
    )
    tenant = TenantColumn(
        verbose_name='租户'
    )
    date_added = tables.DateColumn(
        format="Y-m-d",
        verbose_name='新增日期'
    )
    child_count = tables.Column(
        verbose_name='前缀列表'
    )
    utilization = UtilizationColumn(
        accessor='get_utilization',
        orderable=False,
        verbose_name='使用率'
    )
    description = tables.Column(
        verbose_name='描述'
    )
    tags = TagColumn(
        url_name='ipam:aggregate_list'
    )

    class Meta(BaseTable.Meta):
        model = Aggregate
        fields = ('pk', 'prefix', 'rir', 'tenant', 'child_count', 'utilization', 'date_added', 'description', 'tags')
        default_columns = ('pk', 'prefix', 'rir', 'tenant', 'child_count', 'utilization', 'date_added', 'description')


#
# Roles
#

class RoleTable(BaseTable):
    pk = ToggleColumn()
    name = tables.Column(
        linkify=True,
        verbose_name='名称'
    )
    prefix_count = LinkedCountColumn(
        viewname='ipam:prefix_list',
        url_params={'role_id': 'pk'},
        verbose_name='前缀列表'
    )
    vlan_count = LinkedCountColumn(
        viewname='ipam:vlan_list',
        url_params={'role_id': 'pk'},
        verbose_name='虚拟局域网列表'
    )
    description = tables.Column(
        verbose_name='描述'
    )
    actions = ButtonsColumn(Role)

    class Meta(BaseTable.Meta):
        model = Role
        fields = ('pk', 'name', 'slug', 'prefix_count', 'vlan_count', 'description', 'weight', 'actions')
        default_columns = ('pk', 'name', 'prefix_count', 'vlan_count', 'description', 'actions')


#
# Prefixes
#

class PrefixUtilizationColumn(UtilizationColumn):
    """
    Extend UtilizationColumn to allow disabling the warning & danger thresholds for prefixes
    marked as fully utilized.
    """
    template_code = """
    {% load helpers %}
    {% if record.pk and record.mark_utilized %}
      {% utilization_graph value warning_threshold=0 danger_threshold=0 %}
    {% elif record.pk %}
      {% utilization_graph value %}
    {% endif %}
    """


class PrefixTable(BaseTable):
    pk = ToggleColumn()
    prefix = tables.TemplateColumn(
        template_code=PREFIX_LINK,
        attrs={'td': {'class': 'text-nowrap'}},
        verbose_name='前缀'
    )
    prefix_flat = tables.TemplateColumn(
        template_code=PREFIXFLAT_LINK,
        attrs={'td': {'class': 'text-nowrap'}},
        verbose_name='Prefix (Flat)',
    )
    depth = tables.Column(
        accessor=Accessor('_depth'),
        verbose_name='Depth'
    )
    children = LinkedCountColumn(
        accessor=Accessor('_children'),
        viewname='ipam:prefix_list',
        url_params={
            'vrf_id': 'vrf_id',
            'within': 'prefix',
        },
        verbose_name='子前缀列表'
    )
    status = ChoiceFieldColumn(
        default=AVAILABLE_LABEL,
        verbose_name='状态'
    )
    vrf = tables.TemplateColumn(
        template_code=VRF_LINK,
        verbose_name='虚拟路由和转发'
    )
    tenant = TenantColumn(
        verbose_name='租户'
    )
    site = tables.Column(
        linkify=True,
        verbose_name='站点'
    )
    vlan = tables.Column(
        linkify=True,
        verbose_name='虚拟局域网'
    )
    role = tables.Column(
        linkify=True,
        verbose_name='角色'
    )
    is_pool = BooleanColumn(
        verbose_name='Pool'
    )
    mark_utilized = BooleanColumn(
        verbose_name='Marked Utilized'
    )
    utilization = PrefixUtilizationColumn(
        accessor='get_utilization',
        orderable=False,
        verbose_name='使用率'
    )
    description = tables.Column(
        verbose_name='描述'
    )
    tags = TagColumn(
        url_name='ipam:prefix_list'
    )

    class Meta(BaseTable.Meta):
        model = Prefix
        fields = (
            'pk', 'prefix', 'prefix_flat', 'status', 'children', 'vrf', 'utilization', 'tenant', 'site', 'vlan', 'role',
            'is_pool', 'mark_utilized', 'description', 'tags',
        )
        default_columns = (
            'pk', 'prefix', 'status', 'children', 'vrf', 'utilization', 'tenant', 'site', 'vlan', 'role', 'description',
        )
        row_attrs = {
            'class': lambda record: 'success' if not record.pk else '',
        }


#
# IP ranges
#

class IPRangeTable(BaseTable):
    pk = ToggleColumn()
    start_address = tables.Column(
        linkify=True,
        verbose_name='起始地址'
    )
    end_address = tables.Column(
        verbose_name='结束地址'
    )
    size = tables.Column(
        verbose_name='大小'
    )
    vrf = tables.TemplateColumn(
        template_code=VRF_LINK,
        verbose_name='虚拟路由和转发'
    )
    status = ChoiceFieldColumn(
        default=AVAILABLE_LABEL,
        verbose_name='状态'
    )
    role = tables.Column(
        linkify=True,
        verbose_name='角色'
    )
    tenant = TenantColumn(
        verbose_name='租户'
    )
    description = tables.Column(
        verbose_name='描述'
    )
    utilization = UtilizationColumn(
        accessor='utilization',
        orderable=False
    )

    class Meta(BaseTable.Meta):
        model = IPRange
        fields = (
            'pk', 'start_address', 'end_address', 'size', 'vrf', 'status', 'role', 'tenant', 'description',
            'utilization',
        )
        default_columns = (
            'pk', 'start_address', 'end_address', 'size', 'vrf', 'status', 'role', 'tenant', 'description',
        )
        row_attrs = {
            'class': lambda record: 'success' if not record.pk else '',
        }


#
# IPAddresses
#

class IPAddressTable(BaseTable):
    
    pk = ToggleColumn()
    address = tables.TemplateColumn(
        template_code=IPADDRESS_LINK,
        verbose_name='IP地址'
    )
    vrf = tables.TemplateColumn(
        template_code=VRF_LINK,
        verbose_name='虚拟路由和转发'
    )
    status = ChoiceFieldColumn(
        default=AVAILABLE_LABEL,
        verbose_name='状态'
    )
    role = ChoiceFieldColumn(
        verbose_name='角色'
    )
    tenant = TenantColumn(
        verbose_name='租户'
    )
    dns_name = tables.Column(
        verbose_name='网域名称'
    )
    description = tables.Column(
        verbose_name='描述'
    )
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name='Interface'
    )
    assigned_object_parent = tables.Column(
        accessor='assigned_object.parent_object',
        linkify=True,
        orderable=False,
        verbose_name='Device/VM'
    )
    nat_inside = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name='NAT (Inside)'
    )
    assigned = BooleanColumn(
        accessor='assigned_object',
        linkify=True,
        verbose_name='已分配'
    )
    tags = TagColumn(
        url_name='ipam:ipaddress_list'
    )

    class Meta(BaseTable.Meta):
        model = IPAddress
        fields = (
            'pk', 'address', 'vrf', 'status', 'role', 'tenant', 'nat_inside', 'assigned', 'dns_name', 'description',
            'tags',
        )
        default_columns = (
            'pk', 'address', 'vrf', 'status', 'role', 'tenant', 'assigned', 'dns_name', 'description',
        )
        row_attrs = {
            'class': lambda record: 'success' if not isinstance(record, IPAddress) else '',
        }


class IPAddressAssignTable(BaseTable):
    address = tables.TemplateColumn(
        template_code=IPADDRESS_ASSIGN_LINK,
        verbose_name='IP Address'
    )
    status = ChoiceFieldColumn()
    assigned_object = tables.Column(
        orderable=False
    )

    class Meta(BaseTable.Meta):
        model = IPAddress
        fields = ('address', 'dns_name', 'vrf', 'status', 'role', 'tenant', 'assigned_object', 'description')
        orderable = False


class InterfaceIPAddressTable(BaseTable):
    """
    List IP addresses assigned to a specific Interface.
    """
    address = tables.Column(
        linkify=True,
        verbose_name='IP Address'
    )
    vrf = tables.TemplateColumn(
        template_code=VRF_LINK,
        verbose_name='VRF'
    )
    status = ChoiceFieldColumn()
    tenant = TenantColumn()
    actions = ButtonsColumn(
        model=IPAddress
    )

    class Meta(BaseTable.Meta):
        model = IPAddress
        fields = ('address', 'vrf', 'status', 'role', 'tenant', 'description')
