import django_tables2 as tables
from django.conf import settings

from utilities.tables import (
    BaseTable, BooleanColumn, ButtonsColumn, ChoiceFieldColumn, ColorColumn, ContentTypeColumn, ContentTypesColumn,
    MarkdownColumn, ToggleColumn,
)
from .models import *

__all__ = (
    'ConfigContextTable',
    'CustomFieldTable',
    'CustomLinkTable',
    'ExportTemplateTable',
    'JournalEntryTable',
    'ObjectChangeTable',
    'ObjectJournalTable',
    'TaggedItemTable',
    'TagTable',
    'WebhookTable',
)

CONFIGCONTEXT_ACTIONS = """
{% if perms.extras.change_configcontext %}
    <a href="{% url 'extras:configcontext_edit' pk=record.pk %}" class="btn btn-sm btn-warning"><i class="mdi mdi-pencil" aria-hidden="true"></i></a>
{% endif %}
{% if perms.extras.delete_configcontext %}
    <a href="{% url 'extras:configcontext_delete' pk=record.pk %}" class="btn btn-sm btn-danger"><i class="mdi mdi-trash-can-outline" aria-hidden="true"></i></a>
{% endif %}
"""

OBJECTCHANGE_OBJECT = """
{% if record.changed_object.get_absolute_url %}
    <a href="{{ record.changed_object.get_absolute_url }}">{{ record.object_repr }}</a>
{% else %}
    {{ record.object_repr }}
{% endif %}
"""

OBJECTCHANGE_REQUEST_ID = """
<a href="{% url 'extras:objectchange_list' %}?request_id={{ value }}">{{ value }}</a>
"""


#
# Custom fields
#

class CustomFieldTable(BaseTable):
    pk = ToggleColumn()
    name = tables.Column(
        linkify=True,
        verbose_name='名称'
    )
    content_types = ContentTypesColumn(
        verbose_name='内容类型'
    )
    label = tables.Column(
        verbose_name='标签'
    )
    type = tables.Column(
        verbose_name='类型'
    )
    required = BooleanColumn(
        verbose_name='必要'
    )
    description = tables.Column(
        verbose_name='描述'
    )

    class Meta(BaseTable.Meta):
        model = CustomField
        fields = (
            'pk', 'name', 'content_types', 'label', 'type', 'required', 'weight', 'default', 'description',
            'filter_logic', 'choices',
        )
        default_columns = ('pk', 'name', 'content_types', 'label', 'type', 'required', 'description')


#
# Custom links
#

class CustomLinkTable(BaseTable):
    pk = ToggleColumn()
    name = tables.Column(
        linkify=True,
        verbose_name='名称'
    )
    content_type = ContentTypeColumn(
        verbose_name='内容类型'
    )
    group_name = tables.Column(
        verbose_name='群组名称'
    )
    button_class = tables.Column(
        verbose_name='按钮类型'
    )
    new_window = BooleanColumn(
        verbose_name='新窗口'
    )

    class Meta(BaseTable.Meta):
        model = CustomLink
        fields = (
            'pk', 'name', 'content_type', 'link_text', 'link_url', 'weight', 'group_name', 'button_class', 'new_window',
        )
        default_columns = ('pk', 'name', 'content_type', 'group_name', 'button_class', 'new_window')


#
# Export templates
#

class ExportTemplateTable(BaseTable):
    pk = ToggleColumn()
    name = tables.Column(
        linkify=True,
        verbose_name='名称'
    )
    content_type = ContentTypeColumn(
        verbose_name='内容类型'
    )
    description = tables.Column(
        verbose_name='描述'
    )
    mime_type = tables.Column(
        verbose_name='MIME类型'
    )
    file_extension = tables.Column(
        verbose_name='文件扩展名'
    )
    as_attachment = BooleanColumn(
        verbose_name='附件下载'
    )

    class Meta(BaseTable.Meta):
        model = ExportTemplate
        fields = (
            'pk', 'name', 'content_type', 'description', 'mime_type', 'file_extension', 'as_attachment',
        )
        default_columns = (
            'pk', 'name', 'content_type', 'description', 'mime_type', 'file_extension', 'as_attachment',
        )


#
# Webhooks
#

class WebhookTable(BaseTable):
    pk = ToggleColumn()
    name = tables.Column(
        linkify=True,
        verbose_name='名称'
    )
    content_types = ContentTypesColumn(
        verbose_name='目标类型'
    )
    enabled = BooleanColumn(
        verbose_name='已启用'
    )
    type_create = BooleanColumn(
        verbose_name='创建'
    )
    type_update = BooleanColumn(
        verbose_name='更新'
    )
    type_delete = BooleanColumn(
        verbose_name='删除'
    )
    http_method = tables.Column(
        verbose_name='HTTP方法'
    )
    payload_url = tables.Column(
        verbose_name='网址'
    )
    ssl_validation = BooleanColumn(
        verbose_name='SSL Validation'
    )

    class Meta(BaseTable.Meta):
        model = Webhook
        fields = (
            'pk', 'name', 'content_types', 'enabled', 'type_create', 'type_update', 'type_delete', 'http_method',
            'payload_url', 'secret', 'ssl_validation', 'ca_file_path',
        )
        default_columns = (
            'pk', 'name', 'content_types', 'enabled', 'type_create', 'type_update', 'type_delete', 'http_method',
            'payload_url',
        )


#
# Tags
#

class TagTable(BaseTable):
    pk = ToggleColumn()
    name = tables.Column(
        linkify=True,
        verbose_name='名称'
    )
    items = tables.Column(
        verbose_name='项目'
    )
    color = ColorColumn(
        verbose_name='颜色'
    )
    description = tables.Column(
        verbose_name='描述'
    )
    actions = ButtonsColumn(Tag)

    class Meta(BaseTable.Meta):
        model = Tag
        fields = ('pk', 'name', 'items', 'slug', 'color', 'description', 'actions')


class TaggedItemTable(BaseTable):
    content_type = ContentTypeColumn(
        verbose_name='Type'
    )
    content_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name='Object'
    )

    class Meta(BaseTable.Meta):
        model = TaggedItem
        fields = ('content_type', 'content_object')


class ConfigContextTable(BaseTable):
    pk = ToggleColumn()
    name = tables.Column(
        linkify=True,
        verbose_name='名称'
    )
    weight = tables.Column(
        verbose_name='权重'
    )
    is_active = BooleanColumn(
        verbose_name='激活'
    )
    description = tables.Column(
        verbose_name='描述'
    )

    class Meta(BaseTable.Meta):
        model = ConfigContext
        fields = (
            'pk', 'name', 'weight', 'is_active', 'description', 'regions', 'sites', 'roles', 'platforms',
            'cluster_groups', 'clusters', 'tenant_groups', 'tenants',
        )
        default_columns = ('pk', 'name', 'weight', 'is_active', 'description')


class ObjectChangeTable(BaseTable):
    time = tables.DateTimeColumn(
        linkify=True,
        format=settings.SHORT_DATETIME_FORMAT,
        verbose_name='时间'
    )
    user_name = tables.Column(
        verbose_name='用户名'
    )
    action = ChoiceFieldColumn(
        verbose_name='行动'
    )
    changed_object_type = ContentTypeColumn(
        verbose_name='目标类型'
    )
    object_repr = tables.TemplateColumn(
        template_code=OBJECTCHANGE_OBJECT,
        verbose_name='目标'
    )
    request_id = tables.TemplateColumn(
        template_code=OBJECTCHANGE_REQUEST_ID,
        verbose_name='请求ID'
    )

    class Meta(BaseTable.Meta):
        model = ObjectChange
        fields = ('time', 'user_name', 'action', 'changed_object_type', 'object_repr', 'request_id')


class ObjectJournalTable(BaseTable):
    """
    Used for displaying a set of JournalEntries within the context of a single object.
    """
    created = tables.DateTimeColumn(
        linkify=True,
        format=settings.SHORT_DATETIME_FORMAT,
        verbose_name='创建日期'
    )
    kind = ChoiceFieldColumn(
        verbose_name='种类'
    )
    comments = tables.TemplateColumn(
        template_code='{% load helpers %}{{ value|render_markdown|truncatewords_html:50 }}'
    )
    actions = ButtonsColumn(
        model=JournalEntry
    )

    class Meta(BaseTable.Meta):
        model = JournalEntry
        fields = ('created', 'created_by', 'kind', 'comments', 'actions')


class JournalEntryTable(ObjectJournalTable):
    pk = ToggleColumn()
    created_by = tables.Column(
        verbose_name='创建者'
    )
    assigned_object_type = ContentTypeColumn(
        verbose_name='目标类型'
    )
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name='目标'
    )
    comments = MarkdownColumn(
        verbose_name='评论'
    )

    class Meta(BaseTable.Meta):
        model = JournalEntry
        fields = (
            'pk', 'created', 'created_by', 'assigned_object_type', 'assigned_object', 'kind', 'comments', 'actions'
        )
