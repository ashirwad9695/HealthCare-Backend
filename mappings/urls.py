from django.urls import path
from .views import MappingListCreateView, MappingDetailOrPatientMappingsView

urlpatterns = [
    path('', MappingListCreateView.as_view(), name='mapping_list_create'),
    path('<int:id>/', MappingDetailOrPatientMappingsView.as_view(), name='mapping_detail_or_patient'),
]
