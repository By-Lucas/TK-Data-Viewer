
from django.urls import path

from data_viewer.views import data_views

tag_name = "data_viewer"

urlpatterns = [
    path('upload-data/', data_views.import_csv_xlsx, name='upload_data'),
    path('remove-duplicates-data/', data_views.remove_duplicates, name='remove_duplicates'),
    path('save-changes-data/', data_views.save_changes, name='save_changes'),
    path('ajax-data-pagination/', data_views.ajax_data_pagination, name='ajax_data_pagination'),

]
