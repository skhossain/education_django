from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from .paginationviews import *

urlpatterns = [
  path('apiedu-studentinfoPagination-api/', StudentPaginationApiview, name='apiedu-studentinfoPagination-api'),

]