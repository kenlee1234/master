from django import forms
from django.utils.translation import gettext as _

from extras.forms import CustomFieldModelFilterForm
from tenancy.models import Tenant, TenantGroup
from utilities.forms import BootstrapMixin, DynamicModelMultipleChoiceField, TagFilterField


class TenantGroupFilterForm(BootstrapMixin, CustomFieldModelFilterForm):
    model = TenantGroup
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('所有字段')}),
        label=_('搜索')
    )
    parent_id = DynamicModelMultipleChoiceField(
        queryset=TenantGroup.objects.all(),
        required=False,
        label=_('所属分组'),
        fetch_trigger='open'
    )


class TenantFilterForm(BootstrapMixin, CustomFieldModelFilterForm):
    model = Tenant
    field_groups = (
        ('q', 'tag'),
        ('group_id',),
    )
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('所有字段')}),
        label=_('搜索')
    )
    group_id = DynamicModelMultipleChoiceField(
        queryset=TenantGroup.objects.all(),
        required=False,
        null_option='None',
        label=_('分组'),
        fetch_trigger='open'
    )
    tag = TagFilterField(model)
