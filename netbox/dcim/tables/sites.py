import django_tables2 as tables

from dcim.models import Location, Region, Site, SiteGroup
from tenancy.tables import TenantColumn
from utilities.tables import (
    BaseTable, ButtonsColumn, ChoiceFieldColumn, LinkedCountColumn, MarkdownColumn, MPTTColumn, TagColumn, ToggleColumn,
)
from .template_code import LOCATION_ELEVATIONS

__all__ = (
    'LocationTable',
    'RegionTable',
    'SiteTable',
    'SiteGroupTable',
)


#
# Regions
#

class RegionTable(BaseTable):
    pk = ToggleColumn()
    name = MPTTColumn(
        linkify=True,
        verbose_name='名称'
    )
    site_count = LinkedCountColumn(
        viewname='dcim:site_list',
        url_params={'region_id': 'pk'},
        verbose_name='站点列表'
    )
    description = tables.Column(
        verbose_name='描述'
    )
    actions = ButtonsColumn(Region)

    class Meta(BaseTable.Meta):
        model = Region
        fields = ('pk', 'name', 'slug', 'site_count', 'description', 'actions')
        default_columns = ('pk', 'name', 'site_count', 'description', 'actions')


#
# Site groups
#

class SiteGroupTable(BaseTable):
    pk = ToggleColumn()
    name = MPTTColumn(
        linkify=True,
        verbose_name='名称'
    )
    site_count = LinkedCountColumn(
        viewname='dcim:site_list',
        url_params={'group_id': 'pk'},
        verbose_name='站点列表'
    )
    description = tables.Column(
        verbose_name='描述'
    )
    actions = ButtonsColumn(SiteGroup)

    class Meta(BaseTable.Meta):
        model = SiteGroup
        fields = ('pk', 'name', 'slug', 'site_count', 'description', 'actions')
        default_columns = ('pk', 'name', 'site_count', 'description', 'actions')


#
# Sites
#

class SiteTable(BaseTable):
    pk = ToggleColumn()
    name = tables.Column(
        linkify=True,
        verbose_name='名称'
    )
    status = ChoiceFieldColumn(
        verbose_name='状态'
    )
    facility = tables.Column(
        verbose_name='设施'
    )
    region = tables.Column(
        linkify=True,
        verbose_name='地区'
    )
    group = tables.Column(
        linkify=True,
        verbose_name='群组'
    )
    tenant = TenantColumn(
        verbose_name='租户'
    )
    asn = tables.Column(
        verbose_name='自治系统编号'
    )
    description = tables.Column(
        verbose_name='描述'
    )
    comments = MarkdownColumn()
    tags = TagColumn(
        url_name='dcim:site_list'
    )

    class Meta(BaseTable.Meta):
        model = Site
        fields = (
            'pk', 'name', 'slug', 'status', 'facility', 'region', 'group', 'tenant', 'asn', 'time_zone', 'description',
            'physical_address', 'shipping_address', 'latitude', 'longitude', 'contact_name', 'contact_phone',
            'contact_email', 'comments', 'tags',
        )
        default_columns = ('pk', 'name', 'status', 'facility', 'region', 'group', 'tenant', 'asn', 'description')


#
# Locations
#

class LocationTable(BaseTable):
    pk = ToggleColumn()
    name = MPTTColumn(
        linkify=True,
        verbose_name='名称'
    )
    site = tables.Column(
        linkify=True,
        verbose_name='站点'
    )
    rack_count = LinkedCountColumn(
        viewname='dcim:rack_list',
        url_params={'location_id': 'pk'},
        verbose_name='机架列表'
    )
    device_count = LinkedCountColumn(
        viewname='dcim:device_list',
        url_params={'location_id': 'pk'},
        verbose_name='设备列表'
    )
    description = tables.Column(
        verbose_name='描述'
    )
    actions = ButtonsColumn(
        model=Location,
        prepend_template=LOCATION_ELEVATIONS
    )

    class Meta(BaseTable.Meta):
        model = Location
        fields = ('pk', 'name', 'site', 'rack_count', 'device_count', 'description', 'slug', 'actions')
        default_columns = ('pk', 'name', 'site', 'rack_count', 'device_count', 'description', 'actions')
