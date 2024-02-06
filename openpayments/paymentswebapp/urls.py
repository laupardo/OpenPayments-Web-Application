from django.urls import path
from .views import SearchExportView,TypeaheadDataView

urlpatterns = [
    path('search/', SearchExportView.as_view(), name='search'),
    path('typeahead/', TypeaheadDataView.as_view(), name='typeahead_data'),
]