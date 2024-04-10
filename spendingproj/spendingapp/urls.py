from django.urls import path
from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.spending, name='spending'),
    path('adauga/', views.adauga, name='adauga'),
    path('select_day_data/', views.select_day_data, name='select_day_data'),
    path('select_range_data/', views.select_range_data, name='select_range_data'),
    path('export/', views.export, name='export'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

