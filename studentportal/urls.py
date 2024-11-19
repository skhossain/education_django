from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('wellcome', wellcome.as_view(), name='wellcome'),
    path('admission', admission.as_view(), name='admission'),
    path('admission-form', admission_form.as_view(), name='admission-form'),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)