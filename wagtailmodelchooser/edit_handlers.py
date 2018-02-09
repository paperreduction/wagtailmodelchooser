from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from wagtail.admin.edit_handlers import BaseChooserPanel

from .widgets import AdminModelChooser

FILTERS = {}


class ModelChooserPanel(BaseChooserPanel):
    filter_name = None

    def __init__(self, *args, **kwargs):
        filter_name = kwargs.pop('filter_name', None)
        self.filter_name = filter_name
        if filter_name is not None:
            FILTERS[filter_name] = filter_name

        super().__init__(*args, **kwargs)

    def bind_to_model(self, model):
        new = self.clone()
        new.model = model
        new.field_name = self.field_name
        new.filter_name = self.filter_name
        new.widget = self.widget
        new.on_model_bound()
        return new

    def widget_overrides(self):
        if hasattr(self, 'widget'):
            return {
                self.field_name: self.widget(
                    self.target_model(),
                    filter_name=self.filter_name
                )
            }

        return {
            self.field_name: AdminModelChooser(
                self.target_model(),
                filter_name=self.filter_name
            )
        }

    def target_model(self):
        return self.db_field.remote_field.model

    def render_as_field(self):
        instance_obj = self.get_chosen_item()
        return mark_safe(render_to_string(self.field_template, {
            'field': self.bound_field,
            'instance': instance_obj,
        }))
