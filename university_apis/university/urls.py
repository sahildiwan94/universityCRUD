from . import views
from django.urls import path


"""
The urlpatterns list routes URLs to views of university app.
"""
urlpatterns = [

	path('', views.UniversityCreateList.as_view(), name='university_create_list'),
	path('<int:university_id>', views.UniversityRetrieveUpdateDelete.as_view(), name='university_retrieve_update_delete'),
	path('search', views.UniversitySearch.as_view({'get': 'list'}), name='university_search'),

]


