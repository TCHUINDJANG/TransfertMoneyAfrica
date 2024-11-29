import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuditsConfig(AppConfig):
    name = "audits"
    verbose_name = _("Audits")

    def ready(self):
        with contextlib.suppress(ImportError):
            import cash_send.audits.signal
