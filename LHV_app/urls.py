from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from source_utils.permission_mixins import TemporaryPassWordTemplateView

from django.contrib import admin


urlpatterns = [
    url(r"^$", TemporaryPassWordTemplateView.as_view(
        template_name="homepage.html"), name="home"
    ),
    url(r"^403/", TemplateView.as_view(
        template_name="403.html"), name="403"
    ),
    url(r"^404/", TemplateView.as_view(
        template_name="403.html"), name="404"
    ),
    url(r"^500/", TemplateView.as_view(
        template_name="403.html"), name="500"
    ),
    url(r"^temporary_password_reset/", TemplateView.as_view(
        template_name="temp_password_change.html"), name="temp_password_change"
    ),
    url(r"^dgrt/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
    url(r"^company/", include("company.urls")),
    url(r"^customer_finance/", include("customer_finance.urls")),
    url(r"^equipment/", include("equipment.urls")),
    url(r"^finance/", include("finance.urls")),
    url(r"^operation_finance/", include("operation_finance.urls")),
    url(r'^schedule/', include('schedule.urls')),
    url(r"^service/", include("service.urls")),
    url(r"^stock/", include("stock.urls")),
    url(r'^time_log/', include('time_log.urls')),
    url(r"^work_order/", include("work_order.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
