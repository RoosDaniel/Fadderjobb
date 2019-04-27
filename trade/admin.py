from django.contrib import admin, messages
from django.http import HttpResponseRedirect

from .models import Trade


class TradeAdmin(admin.ModelAdmin):
    model = Trade

    list_display = ("__str__", "sender", "receiver", "completed")

    search_fields = ("sender", "receiver")

    list_filter = ("completed",)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context.update({'help_text': 'Sökbara fält: sändare, mottagare.'})

        return super(TradeAdmin, self)\
            .changelist_view(request, extra_context=extra_context)

    def response_change(self, request, obj):
        if "_accept_trade" in request.POST:
            obj.accept()

            messages.add_message(request, messages.INFO, "Bytet har nu genomförts.")

            return HttpResponseRedirect(".")

        return super().response_change(request, obj)

admin.site.register(Trade, TradeAdmin)
