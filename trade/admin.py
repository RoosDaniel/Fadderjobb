from django.contrib import admin

from .models import Trade


class TradeAdmin(admin.ModelAdmin):
    model = Trade

    list_display = ("__str__", "sender", "receiver")

    search_fields = ("sender", "receiver")

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context.update({'help_text': 'Sökbara fält: sändare, mottagare.'})

        return super(TradeAdmin, self)\
            .changelist_view(request, extra_context=extra_context)

admin.site.register(Trade, TradeAdmin)
