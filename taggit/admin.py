from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from taggit.models import Tag, TaggedItem

class ContentTypeFilter(admin.SimpleListFilter):
    """Only displays content types that have been used by a TaggedItem."""
    title = _("content type")
    parameter_name = "content"

    def lookups(self, request, model_admin):
        content_types = TaggedItem.objects.all().values_list('content_type__name', flat=True).distinct()
        return [(content_type, content_type) for content_type in content_types]

    def queryset(self, request, queryset):
        # If the filter is set to "All", value() will be None.
        if self.value():
            return queryset.filter(content_type__name=self.value())

class UsedTagFilter(admin.SimpleListFilter):
    """Only displays Tags that have been used within the model instances."""
    title = _("tags")
    parameter_name = "tag"

    def lookups(self, request, model_admin):
        content_type = ContentType.objects.get_for_model(model_admin.model)
        tags = TaggedItem.objects.filter(content_type=content_type)
        if tags:
            tags = tags.values_list('tag__name', flat=True).distinct()

        return [(tag, tag) for tag in tags]

    def queryset(self, request, queryset):
        # If the filter is set to "All", value() will be None.
        if self.value():
            return queryset.filter(tags__name=self.value())

class TaggedItemInline(admin.StackedInline):
    model = TaggedItem

class TaggedItemAdmin(admin.ModelAdmin):
    list_display = ["id", "tag", "object_id", "content_type"]
    list_filter = [ContentTypeFilter, "tag"]

class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    ordering = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ["name"]}


admin.site.register(TaggedItem, TaggedItemAdmin)
admin.site.register(Tag, TagAdmin)
