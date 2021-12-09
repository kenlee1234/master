import django_tables2 as tables
from django_tables2.utils import Accessor

from utilities.tables import BaseTable, BooleanColumn
from dcim.models import ConsolePort, Interface, PowerPort
from .cables import *
from .devices import *
from .devicetypes import *
from .power import *
from .racks import *
from .sites import *


#
# Device connections
#

class ConsoleConnectionTable(BaseTable):
    console_server = tables.Column(
        accessor=Accessor('_path__destination__device'),
        orderable=False,
        linkify=True,
        verbose_name='控制台服务器'
    )
    console_server_port = tables.Column(
        accessor=Accessor('_path__destination'),
        orderable=False,
        linkify=True,
        verbose_name='端口'
    )
    device = tables.Column(
        linkify=True,
        verbose_name='設備'
    )
    name = tables.Column(
        linkify=True,
        verbose_name='控制台端口'
    )
    reachable = BooleanColumn(
        accessor=Accessor('_path__is_active'),
        verbose_name='可连接'
    )

    class Meta(BaseTable.Meta):
        model = ConsolePort
        fields = ('device', 'name', 'console_server', 'console_server_port', 'reachable')


class PowerConnectionTable(BaseTable):
    pdu = tables.Column(
        accessor=Accessor('_path__destination__device'),
        orderable=False,
        linkify=True,
        verbose_name='电力分配单元'
    )
    outlet = tables.Column(
        accessor=Accessor('_path__destination'),
        orderable=False,
        linkify=True,
        verbose_name='电源插口'
    )
    device = tables.Column(
        linkify=True,
        verbose_name='设备'
    )
    name = tables.Column(
        linkify=True,
        verbose_name='电源端口'
    )
    reachable = BooleanColumn(
        accessor=Accessor('_path__is_active'),
        verbose_name='可连接'
    )

    class Meta(BaseTable.Meta):
        model = PowerPort
        fields = ('device', 'name', 'pdu', 'outlet', 'reachable')


class InterfaceConnectionTable(BaseTable):
    device_a = tables.Column(
        accessor=Accessor('device'),
        linkify=True,
        verbose_name='A设备'
    )
    interface_a = tables.Column(
        accessor=Accessor('name'),
        linkify=True,
        verbose_name='A接口'
    )
    device_b = tables.Column(
        accessor=Accessor('_path__destination__device'),
        orderable=False,
        linkify=True,
        verbose_name='B设备'
    )
    interface_b = tables.Column(
        accessor=Accessor('_path__destination'),
        orderable=False,
        linkify=True,
        verbose_name='B接口'
    )
    reachable = BooleanColumn(
        accessor=Accessor('_path__is_active'),
        verbose_name='可连接'
    )

    class Meta(BaseTable.Meta):
        model = Interface
        fields = ('device_a', 'interface_a', 'device_b', 'interface_b', 'reachable')
