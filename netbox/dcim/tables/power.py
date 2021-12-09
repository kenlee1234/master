import django_tables2 as tables

from dcim.models import PowerFeed, PowerPanel
from utilities.tables import BaseTable, ChoiceFieldColumn, LinkedCountColumn, MarkdownColumn, TagColumn, ToggleColumn
from .devices import CableTerminationTable

__all__ = (
    'PowerFeedTable',
    'PowerPanelTable',
)


#
# Power panels
#

class PowerPanelTable(BaseTable):
    pk = ToggleColumn()
    name = tables.Column(
        linkify=True,
        verbose_name='名称'
    )
    site = tables.Column(
        linkify=True,
        verbose_name='站点'
    )
    location = tables.Column(
        verbose_name='地点'
    )
    powerfeed_count = LinkedCountColumn(
        viewname='dcim:powerfeed_list',
        url_params={'power_panel_id': 'pk'},
        verbose_name='供电列表'
    )
    tags = TagColumn(
        url_name='dcim:powerpanel_list'
    )

    class Meta(BaseTable.Meta):
        model = PowerPanel
        fields = ('pk', 'name', 'site', 'location', 'powerfeed_count', 'tags')
        default_columns = ('pk', 'name', 'site', 'location', 'powerfeed_count')


#
# Power feeds
#

# We're not using PathEndpointTable for PowerFeed because power connections
# cannot traverse pass-through ports.
class PowerFeedTable(CableTerminationTable):
    pk = ToggleColumn()
    name = tables.Column(
        linkify=True,
        verbose_name='名称'
    )
    power_panel = tables.Column(
        linkify=True,
        verbose_name='电源面板'
    )
    rack = tables.Column(
        linkify=True,
        verbose_name='机架'
    )
    status = ChoiceFieldColumn(
        verbose_name='状态'
    )
    type = ChoiceFieldColumn(
        verbose_name='类型'
    )
    supply = tables.Column(
        verbose_name='供给'
    )
    voltage = tables.Column(
        verbose_name='伏特'
    )
    amperage = tables.Column(
        verbose_name='安培'
    )
    phase = tables.Column(
        verbose_name='阶段'
    )
    max_utilization = tables.TemplateColumn(
        template_code="{{ value }}%"
    )
    available_power = tables.Column(
        verbose_name='Available power (VA)'
    )
    comments = MarkdownColumn()
    tags = TagColumn(
        url_name='dcim:powerfeed_list'
    )

    class Meta(BaseTable.Meta):
        model = PowerFeed
        fields = (
            'pk', 'name', 'power_panel', 'rack', 'status', 'type', 'supply', 'voltage', 'amperage', 'phase',
            'max_utilization', 'mark_connected', 'cable', 'cable_color', 'cable_peer', 'connection', 'available_power',
            'comments', 'tags',
        )
        default_columns = (
            'pk', 'name', 'power_panel', 'rack', 'status', 'type', 'supply', 'voltage', 'amperage', 'phase', 'cable',
            'cable_peer',
        )
