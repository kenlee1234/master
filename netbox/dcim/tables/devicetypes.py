import django_tables2 as tables

from dcim.models import (
    ConsolePortTemplate, ConsoleServerPortTemplate, DeviceBayTemplate, DeviceType, FrontPortTemplate, InterfaceTemplate,
    Manufacturer, PowerOutletTemplate, PowerPortTemplate, RearPortTemplate,
)
from utilities.tables import (
    BaseTable, BooleanColumn, ButtonsColumn, ColorColumn, LinkedCountColumn, MarkdownColumn, TagColumn, ToggleColumn,
)

__all__ = (
    'ConsolePortTemplateTable',
    'ConsoleServerPortTemplateTable',
    'DeviceBayTemplateTable',
    'DeviceTypeTable',
    'FrontPortTemplateTable',
    'InterfaceTemplateTable',
    'ManufacturerTable',
    'PowerOutletTemplateTable',
    'PowerPortTemplateTable',
    'RearPortTemplateTable',
)


#
# Manufacturers
#

class ManufacturerTable(BaseTable):
    pk = ToggleColumn()
    name = tables.Column(
        linkify=True,
        verbose_name='名称'
    )
    devicetype_count = tables.Column(
        verbose_name='设备类型列表'
    )
    inventoryitem_count = tables.Column(
        verbose_name='清单项目'
    )
    platform_count = tables.Column(
        verbose_name='平台列表'
    )
    description = tables.Column(
        verbose_name='描述'
    )
    slug = tables.Column()
    actions = ButtonsColumn(Manufacturer)

    class Meta(BaseTable.Meta):
        model = Manufacturer
        fields = (
            'pk', 'name', 'devicetype_count', 'inventoryitem_count', 'platform_count', 'description', 'slug', 'actions',
        )


#
# Device types
#

class DeviceTypeTable(BaseTable):
    pk = ToggleColumn()
    model = tables.Column(
        linkify=True,
        verbose_name='设备类型'
    )
    manufacturer = tables.Column(
        verbose_name='制造商'
    )
    part_number = tables.Column(
        verbose_name='部件编号'
    )
    u_height = tables.Column(
        verbose_name='高度（机架单位）'
    )
    is_full_depth = BooleanColumn(
        verbose_name='达到最大深度'
    )
    instance_count = LinkedCountColumn(
        viewname='dcim:device_list',
        url_params={'device_type_id': 'pk'},
        verbose_name='实例列表 '
    )
    comments = MarkdownColumn()
    tags = TagColumn(
        url_name='dcim:devicetype_list'
    )

    class Meta(BaseTable.Meta):
        model = DeviceType
        fields = (
            'pk', 'model', 'manufacturer', 'slug', 'part_number', 'u_height', 'is_full_depth', 'subdevice_role',
            'comments', 'instance_count', 'tags',
        )
        default_columns = (
            'pk', 'model', 'manufacturer', 'part_number', 'u_height', 'is_full_depth', 'instance_count',
        )


#
# Device type components
#

class ComponentTemplateTable(BaseTable):
    pk = ToggleColumn()
    name = tables.Column(
        order_by=('_name',)
    )


class ConsolePortTemplateTable(ComponentTemplateTable):
    actions = ButtonsColumn(
        model=ConsolePortTemplate,
        buttons=('edit', 'delete'),
        return_url_extra='%23tab_consoleports'
    )

    class Meta(BaseTable.Meta):
        model = ConsolePortTemplate
        fields = ('pk', 'name', 'label', 'type', 'description', 'actions')
        empty_text = "None"


class ConsoleServerPortTemplateTable(ComponentTemplateTable):
    actions = ButtonsColumn(
        model=ConsoleServerPortTemplate,
        buttons=('edit', 'delete'),
        return_url_extra='%23tab_consoleserverports'
    )

    class Meta(BaseTable.Meta):
        model = ConsoleServerPortTemplate
        fields = ('pk', 'name', 'label', 'type', 'description', 'actions')
        empty_text = "None"


class PowerPortTemplateTable(ComponentTemplateTable):
    actions = ButtonsColumn(
        model=PowerPortTemplate,
        buttons=('edit', 'delete'),
        return_url_extra='%23tab_powerports'
    )

    class Meta(BaseTable.Meta):
        model = PowerPortTemplate
        fields = ('pk', 'name', 'label', 'type', 'maximum_draw', 'allocated_draw', 'description', 'actions')
        empty_text = "None"


class PowerOutletTemplateTable(ComponentTemplateTable):
    actions = ButtonsColumn(
        model=PowerOutletTemplate,
        buttons=('edit', 'delete'),
        return_url_extra='%23tab_poweroutlets'
    )

    class Meta(BaseTable.Meta):
        model = PowerOutletTemplate
        fields = ('pk', 'name', 'label', 'type', 'power_port', 'feed_leg', 'description', 'actions')
        empty_text = "None"


class InterfaceTemplateTable(ComponentTemplateTable):
    mgmt_only = BooleanColumn(
        verbose_name='Management Only'
    )
    actions = ButtonsColumn(
        model=InterfaceTemplate,
        buttons=('edit', 'delete'),
        return_url_extra='%23tab_interfaces'
    )

    class Meta(BaseTable.Meta):
        model = InterfaceTemplate
        fields = ('pk', 'name', 'label', 'mgmt_only', 'type', 'description', 'actions')
        empty_text = "None"


class FrontPortTemplateTable(ComponentTemplateTable):
    rear_port_position = tables.Column(
        verbose_name='Position'
    )
    color = ColorColumn()
    actions = ButtonsColumn(
        model=FrontPortTemplate,
        buttons=('edit', 'delete'),
        return_url_extra='%23tab_frontports'
    )

    class Meta(BaseTable.Meta):
        model = FrontPortTemplate
        fields = ('pk', 'name', 'label', 'type', 'color', 'rear_port', 'rear_port_position', 'description', 'actions')
        empty_text = "None"


class RearPortTemplateTable(ComponentTemplateTable):
    color = ColorColumn()
    actions = ButtonsColumn(
        model=RearPortTemplate,
        buttons=('edit', 'delete'),
        return_url_extra='%23tab_rearports'
    )

    class Meta(BaseTable.Meta):
        model = RearPortTemplate
        fields = ('pk', 'name', 'label', 'type', 'color', 'positions', 'description', 'actions')
        empty_text = "None"


class DeviceBayTemplateTable(ComponentTemplateTable):
    actions = ButtonsColumn(
        model=DeviceBayTemplate,
        buttons=('edit', 'delete'),
        return_url_extra='%23tab_devicebays'
    )

    class Meta(BaseTable.Meta):
        model = DeviceBayTemplate
        fields = ('pk', 'name', 'label', 'description', 'actions')
        empty_text = "None"
