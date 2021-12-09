import django_tables2 as tables
from django_tables2.utils import Accessor

from dcim.models import Cable
from utilities.tables import BaseTable, ChoiceFieldColumn, ColorColumn, TagColumn, TemplateColumn, ToggleColumn
from .template_code import CABLE_LENGTH, CABLE_TERMINATION_PARENT

__all__ = (
    'CableTable',
)


#
# Cables
#

class CableTable(BaseTable):
    pk = ToggleColumn()
    id = tables.Column(
        linkify=True,
        verbose_name='ID'
    )
    termination_a_parent = tables.TemplateColumn(
        template_code=CABLE_TERMINATION_PARENT,
        accessor=Accessor('termination_a'),
        orderable=False,
        verbose_name='A方'
    )
    termination_a = tables.Column(
        accessor=Accessor('termination_a'),
        orderable=False,
        linkify=True,
        verbose_name='A终端'
    )
    termination_b_parent = tables.TemplateColumn(
        template_code=CABLE_TERMINATION_PARENT,
        accessor=Accessor('termination_b'),
        orderable=False,
        verbose_name='B方'
    )
    termination_b = tables.Column(
        accessor=Accessor('termination_b'),
        orderable=False,
        linkify=True,
        verbose_name='B终端'
    )
    label = tables.Column(
        verbose_name='标签'
    )
    status = ChoiceFieldColumn(
        verbose_name='状态'
    )
    type = tables.Column(
        verbose_name='类型'
    )
    length = TemplateColumn(
        template_code=CABLE_LENGTH,
        order_by='_abs_length'
    )
    color = ColorColumn()
    tags = TagColumn(
        url_name='dcim:cable_list'
    )

    class Meta(BaseTable.Meta):
        model = Cable
        fields = (
            'pk', 'id', 'label', 'termination_a_parent', 'termination_a', 'termination_b_parent', 'termination_b',
            'status', 'type', 'color', 'length', 'tags',
        )
        default_columns = (
            'pk', 'id', 'label', 'termination_a_parent', 'termination_a', 'termination_b_parent', 'termination_b',
            'status', 'type',
        )
