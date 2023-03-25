
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('data-viewer/', include('data_viewer.urls'), name='data_viewer'),
    
]
