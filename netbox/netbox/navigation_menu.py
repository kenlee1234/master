from dataclasses import dataclass
from typing import Sequence, Optional

from extras.registry import registry
from utilities.choices import ButtonColorChoices


#
# Nav menu data classes
#

@dataclass
class MenuItemButton:

    link: str
    title: str
    icon_class: str
    permissions: Optional[Sequence[str]] = ()
    color: Optional[str] = None


@dataclass
class MenuItem:

    link: str
    link_text: str
    permissions: Optional[Sequence[str]] = ()
    buttons: Optional[Sequence[MenuItemButton]] = ()


@dataclass
class MenuGroup:

    label: str
    items: Sequence[MenuItem]


@dataclass
class Menu:

    label: str
    icon_class: str
    groups: Sequence[MenuGroup]


#
# Utility functions
#

def get_model_item(app_label, model_name, label, actions=('add', 'import')):
    return MenuItem(
        link=f'{app_label}:{model_name}_list',
        link_text=label,
        permissions=[f'{app_label}.view_{model_name}'],
        buttons=get_model_buttons(app_label, model_name, actions)
    )


def get_model_buttons(app_label, model_name, actions=('add', 'import')):
    buttons = []

    if 'add' in actions:
        buttons.append(
            MenuItemButton(
                link=f'{app_label}:{model_name}_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
                permissions=[f'{app_label}.add_{model_name}'],
                color=ButtonColorChoices.GREEN
            )
        )
    if 'import' in actions:
        buttons.append(
            MenuItemButton(
                link=f'{app_label}:{model_name}_import',
                title='Import',
                icon_class='mdi mdi-upload',
                permissions=[f'{app_label}.add_{model_name}'],
                color=ButtonColorChoices.CYAN
            )
        )

    return buttons


#
# Nav menus
#

ORGANIZATION_MENU = Menu(
    label='组织',
    icon_class='mdi mdi-domain',
    groups=(
        MenuGroup(
            label='网站',
            items=(
                get_model_item('dcim', 'site', '站点'),
                get_model_item('dcim', 'region', '范围'),
                get_model_item('dcim', 'sitegroup', '站点分组'),
                get_model_item('dcim', 'location', '地址'),
            ),
        ),
        MenuGroup(
            label='架构',
            items=(
                get_model_item('dcim', 'rack', '架构'),
                get_model_item('dcim', 'rackrole', '架构规则'),
                get_model_item('dcim', 'rackreservation', '保留'),
                MenuItem(
                    link='dcim:rack_elevation_list',
                    link_text='迭代',
                    permissions=['dcim.view_rack']
                ),
            ),
        ),
        MenuGroup(
            label='租户',
            items=(
                get_model_item('tenancy', 'tenant', '租户'),
                get_model_item('tenancy', 'tenantgroup', '租户分组'),
            ),
        ),
    ),
)

DEVICES_MENU = Menu(
    label='设备',
    icon_class='mdi mdi-server',
    groups=(
        MenuGroup(
            label='设备',
            items=(
                get_model_item('dcim', 'device', '设备'),
                get_model_item('dcim', 'devicerole', '设备规则'),
                get_model_item('dcim', 'platform', '平台'),
                get_model_item('dcim', 'virtualchassis', '虚拟机箱'),
            ),
        ),
        MenuGroup(
            label='设备类型',
            items=(
                get_model_item('dcim', 'devicetype', '设备类型'),
                get_model_item('dcim', 'manufacturer', '制造商'),
            ),
        ),
        MenuGroup(
            label='设备组成',
            items=(
                get_model_item('dcim', 'interface', '交互', actions=['import']),
                get_model_item('dcim', 'frontport', '前段端口', actions=['import']),
                get_model_item('dcim', 'rearport', '后端端口', actions=['import']),
                get_model_item('dcim', 'consoleport', '控制台端口', actions=['import']),
                get_model_item('dcim', 'consoleserverport', '控制台服务端口', actions=['import']),
                get_model_item('dcim', 'powerport', '电源端口', actions=['import']),
                get_model_item('dcim', 'poweroutlet', '电源插座', actions=['import']),
                get_model_item('dcim', 'devicebay', '设备托架', actions=['import']),
                get_model_item('dcim', 'inventoryitem', '库存物品', actions=['import']),
            ),
        ),
    ),
)

CONNECTIONS_MENU = Menu(
    label='链接',
    icon_class='mdi mdi-ethernet',
    groups=(
        MenuGroup(
            label='链接',
            items=(
                get_model_item('dcim', 'cable', '线缆', actions=['import']),
                MenuItem(
                    link='dcim:interface_connections_list',
                    link_text='交互链接',
                    permissions=['dcim.view_interface']
                ),
                MenuItem(
                    link='dcim:console_connections_list',
                    link_text='控制台链接',
                    permissions=['dcim.view_consoleport']
                ),
                MenuItem(
                    link='dcim:power_connections_list',
                    link_text='电源链接',
                    permissions=['dcim.view_powerport']
                ),
            ),
        ),
    ),
)

IPAM_MENU = Menu(
    label='IP管理',
    icon_class='mdi mdi-counter',
    groups=(
        MenuGroup(
            label='IP地址',
            items=(
                get_model_item('ipam', 'ipaddress', 'IP地址'),
                get_model_item('ipam', 'iprange', 'IP范围'),
            ),
        ),
        MenuGroup(
            label='前缀',
            items=(
                get_model_item('ipam', 'prefix', '前缀'),
                get_model_item('ipam', 'role', '前缀和VLAN规则'),
            ),
        ),
        MenuGroup(
            label='聚合',
            items=(
                get_model_item('ipam', 'aggregate', '聚合'),
                get_model_item('ipam', 'rir', '区域注册管理'),
            ),
        ),
        MenuGroup(
            label='可验证随机公钥密码',
            items=(
                get_model_item('ipam', 'vrf', '可验证随机公钥密码'),
                get_model_item('ipam', 'routetarget', '路由目标'),
            ),
        ),
        MenuGroup(
            label='虚拟局域网',
            items=(
                get_model_item('ipam', 'vlan', '虚拟局域网'),
                get_model_item('ipam', 'vlangroup', '虚拟局域网分组'),
            ),
        ),
        MenuGroup(
            label='服务',
            items=(
                get_model_item('ipam', 'service', '服务', actions=['import']),
            ),
        ),
    ),
)

VIRTUALIZATION_MENU = Menu(
    label='虚拟化',
    icon_class='mdi mdi-monitor',
    groups=(
        MenuGroup(
            label='Virtual Machines',
            items=(
                get_model_item('virtualization', 'virtualmachine', '虚拟机'),
                get_model_item('virtualization', 'vminterface', '交互', actions=['import']),
            ),
        ),
        MenuGroup(
            label='集群',
            items=(
                get_model_item('virtualization', 'cluster', '集群'),
                get_model_item('virtualization', 'clustertype', '集群类型'),
                get_model_item('virtualization', 'clustergroup', '集群分组'),
            ),
        ),
    ),
)

CIRCUITS_MENU = Menu(
    label='线路',
    icon_class='mdi mdi-transit-connection-variant',
    groups=(
        MenuGroup(
            label='线路',
            items=(
                get_model_item('circuits', 'circuit', '线路'),
                get_model_item('circuits', 'circuittype', '线路类型'),
            ),
        ),
        MenuGroup(
            label='供应商',
            items=(
                get_model_item('circuits', 'provider', '供应商'),
                get_model_item('circuits', 'providernetwork', '供应商网络'),
            ),
        ),
    ),
)

POWER_MENU = Menu(
    label='电源',
    icon_class='mdi mdi-flash',
    groups=(
        MenuGroup(
            label='Power',
            items=(
                get_model_item('dcim', 'powerfeed', '电源供给'),
                get_model_item('dcim', 'powerpanel', '配电盘'),
            ),
        ),
    ),
)

OTHER_MENU = Menu(
    label='其他',
    icon_class='mdi mdi-notification-clear-all',
    groups=(
        MenuGroup(
            label='日志',
            items=(
                get_model_item('extras', 'journalentry', '分录', actions=[]),
                get_model_item('extras', 'objectchange', '变更日志', actions=[]),
            ),
        ),
        MenuGroup(
            label='个性化',
            items=(
                get_model_item('extras', 'customfield', '自定义字段'),
                get_model_item('extras', 'customlink', '自定义链接'),
                get_model_item('extras', 'exporttemplate', '导出模板'),
            ),
        ),
        MenuGroup(
            label='交互',
            items=(
                get_model_item('extras', 'webhook', '微服务API'),
                MenuItem(
                    link='extras:report_list',
                    link_text='报告',
                    permissions=['extras.view_report']
                ),
                MenuItem(
                    link='extras:script_list',
                    link_text='脚本',
                    permissions=['extras.view_script']
                ),
            ),
        ),
        MenuGroup(
            label='其他',
            items=(
                get_model_item('extras', 'tag', '标签'),
                get_model_item('extras', 'configcontext', '配置内容', actions=['add']),
            ),
        ),
    ),
)


MENUS = [
    ORGANIZATION_MENU,
    DEVICES_MENU,
    CONNECTIONS_MENU,
    IPAM_MENU,
    VIRTUALIZATION_MENU,
    CIRCUITS_MENU,
    POWER_MENU,
    OTHER_MENU,
]

#
# Add plugin menus
#

if registry['plugin_menu_items']:
    plugin_menu_groups = []

    for plugin_name, items in registry['plugin_menu_items'].items():
        plugin_menu_groups.append(
            MenuGroup(
                label=plugin_name,
                items=items
            )
        )

    PLUGIN_MENU = Menu(
        label="Plugins",
        icon_class="mdi mdi-puzzle",
        groups=plugin_menu_groups
    )

    MENUS.append(PLUGIN_MENU)
