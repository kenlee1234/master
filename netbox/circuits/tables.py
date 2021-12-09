import django_tables2 as tables
from django_tables2.utils import Accessor

from tenancy.tables import TenantColumn
from utilities.tables import BaseTable, ButtonsColumn, ChoiceFieldColumn, MarkdownColumn, TagColumn, ToggleColumn
from .models import *


__all__ = (
    'CircuitTable',
    'CircuitTypeTable',
    'ProviderTable',
    'ProviderNetworkTable',
)


CIRCUITTERMINATION_LINK = """
{% if value.site %}
  <a href="{{ value.site.get_absolute_url }}">{{ value.site }}</a>
{% elif value.provider_network %}
  <a href="{{ value.provider_network.get_absolute_url }}">{{ value.provider_network }}</a>
{% endif %}
"""


#
# Providers
#

class ProviderTable(BaseTable):
    pk = ToggleColumn()
    name = tables.Column(
        linkify=True,
        verbose_name='名称'
    )
    circuit_count = tables.Column(
        accessor=Accessor('count_circuits'),
        verbose_name='线路'
    )
    asn = tables.Column(
        verbose_name='自治系统编号'
    )
    account = tables.Column(
        verbose_name='帐号'
    )
    comments = MarkdownColumn()
    tags = TagColumn(
        url_name='circuits:provider_list'
    )

    class Meta(BaseTable.Meta):
        model = Provider
        fields = (
            'pk', 'name', 'asn', 'account', 'portal_url', 'noc_contact', 'admin_contact', 'circuit_count', 'comments',
            'tags',
        )
        default_columns = ('pk', 'name', 'asn', 'account', 'circuit_count')


#
# Provider networks
#

class ProviderNetworkTable(BaseTable):
    pk = ToggleColumn()
    name = tables.Column(
        linkify=True,
        verbose_name='名称'
    )
    provider = tables.Column(
        linkify=True,
        verbose_name='运营商'
    )
    description = tables.Column(
        verbose_name='描述'
    )
    comments = MarkdownColumn()
    tags = TagColumn(
        url_name='circuits:providernetwork_list'
    )

    class Meta(BaseTable.Meta):
        model = ProviderNetwork
        fields = ('pk', 'name', 'provider', 'description', 'comments', 'tags')
        default_columns = ('pk', 'name', 'provider', 'description')


#
# Circuit types
#

class CircuitTypeTable(BaseTable):
    pk = ToggleColumn()
    name = tables.Column(
        linkify=True,
        verbose_name='名称'
    )
    circuit_count = tables.Column(
        verbose_name='线路列表'
    )
    description = tables.Column(
        verbose_name='描述'
    )
    actions = ButtonsColumn(CircuitType)

    class Meta(BaseTable.Meta):
        model = CircuitType
        fields = ('pk', 'name', 'circuit_count', 'description', 'slug', 'actions')
        default_columns = ('pk', 'name', 'circuit_count', 'description', 'slug', 'actions')


#
# Circuits
#

class CircuitTable(BaseTable):
    pk = ToggleColumn()
    cid = tables.Column(
        linkify=True,
        verbose_name='ID'
    )
    provider = tables.Column(
        linkify=True,
        verbose_name='运营商'
    )
    type = tables.Column(
        verbose_name='类型'
    )
    status = ChoiceFieldColumn(
        verbose_name='状态'
    )
    tenant = TenantColumn(
        verbose_name='租户'
    )
    termination_a = tables.TemplateColumn(
        template_code=CIRCUITTERMINATION_LINK,
        verbose_name='A终端'
    )
    termination_z = tables.TemplateColumn(
        template_code=CIRCUITTERMINATION_LINK,
        verbose_name='Z终端'
    )
    description = tables.Column(
        verbose_name='描述'
    )
    comments = MarkdownColumn()
    tags = TagColumn(
        url_name='circuits:circuit_list'
    )

    class Meta(BaseTable.Meta):
        model = Circuit
        fields = (
            'pk', 'cid', 'provider', 'type', 'status', 'tenant', 'termination_a', 'termination_z', 'install_date',
            'commit_rate', 'description', 'comments', 'tags',
        )
        default_columns = (
            'pk', 'cid', 'provider', 'type', 'status', 'tenant', 'termination_a', 'termination_z', 'description',
        )
