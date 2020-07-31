from django.shortcuts import render
from rest_framework import generics
from .models import University
from .serializers import UniversitySerializer,UniversityDocumentSerializer
from django.http import JsonResponse
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import UniversityFilter
from .pagination import StandardResultsSetPagination
from .documents import UniversityDocument
from django_countries import countries
from django_elasticsearch_dsl_drf.filter_backends import (
	FilteringFilterBackend,
	OrderingFilterBackend,
	DefaultOrderingFilterBackend
)
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from django_elasticsearch_dsl_drf.constants import (
	LOOKUP_QUERY_ENDSWITH,LOOKUP_QUERY_CONTAINS
)

class UniversityCreateList(generics.ListCreateAPIView):
	"""
	View for creation and listing of Universities.
	"""

	# Queryset,Filter backends,Filterset class,Ordering Fields,Default ordering,Search fields,Serializer class
	queryset = University.objects.filter(isDelete=False)
	filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
	filterset_class = UniversityFilter
	search_fields = ['name']
	ordering_fields = ['name','createdAt']
	ordering = ['-createdAt']
	serializer_class = UniversitySerializer

	def create(self,request,*args,**kwargs):
		"""
		View for Creation of Universities.
		"""

		# Request data
		data = request.data

		# Creation of university object using serializer
		university_obj = UniversitySerializer(data=data)

		try:
			# Transaction block for proper commits and rollbacks
			with transaction.atomic():

				# Validity check of university object
				if university_obj.is_valid():

					# University object saved to database
					university_obj.save()
					response = {"message":"University Created", "data": university_obj.data}
					return JsonResponse(response,status = 201)
				else:
					key = list(university_obj.errors.keys())[0]

					# Error message while validating university object
					try:
						message = (university_obj.errors[key][0]['non_field_errors'])[0]
					except:
						message = university_obj.errors[key][0]
					response = {"message":message, "data": {}}
					return JsonResponse(response, status = 400)
		except Exception as e:

			# Exception occured
			response = {"message":str(e.args[0]), "data": {}}
			return JsonResponse(response, status = 500)

	def list(self,request,*args,**kwargs):
		"""
		View for listing of Universities with pagination,search and filtering functionalities.
		"""

		# Filtering the Queryset by filter Backends
		queryset = self.filter_queryset(self.get_queryset())

		# Paginating the Filtered queryset
		try:
			page = self.paginate_queryset(queryset)
		except:
			data = []
		else:
			if page is not None:
				# Serialized data for a single page
				data = self.get_serializer(page, many=True).data
			else:
				# Serialized data for queryset
				data = self.get_serializer(queryset, many=True).data

		if data:
			message = "Universities Listed"
		else:
			message = "No data available"

		response = {'message':message,'data' : data}
		return JsonResponse(response,status=200)


class UniversityRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
	"""
	View for retrieval,updation and deletion of Universities.
	"""

	def retrieve(self,request,university_id,*args,**kwargs):
		"""
		View for retrieval of Universities.
		"""

		# Fetching university object by id
		try:
			university = University.objects.get(id = university_id , isDelete = False)
		except:
			response = {"message":"Invalid University Id", "data": {}}
			return JsonResponse(response,status = 400)

		# Serialized data of university object
		data = UniversitySerializer(university).data

		if data:
			message = "University Retrieved"
		else:
			message = "No data available"

		response = {'message':message,'data' : data}
		return JsonResponse(response,status=200)

	def update(self,request,university_id,*args,**kwargs):
		"""
		View for Updation of Universities.
		"""

		# Request data
		data = request.data

		# Fetching university object by id
		try:
			university = University.objects.get(id = university_id , isDelete = False)
		except:
			response = {"message":"Invalid University Id", "data": {}}
			return JsonResponse(response,status = 400)

		# Updation of university object using serializer
		university_obj = UniversitySerializer(university,data=data)

		try:
			# Transaction block for proper commits and rollbacks
			with transaction.atomic():

				# Validity check of university object
				if university_obj.is_valid():

					# University object updated
					university_obj.save()
					response = {"message":"University Updated", "data": university_obj.data}
					return JsonResponse(response,status = 200)
				else:
					key = list(university_obj.errors.keys())[0]

					# Error message while validating university object
					try:
						message = (university_obj.errors[key][0]['non_field_errors'])[0]
					except:
						message = university_obj.errors[key][0]
					response = {"message":message, "data": {}}
					return JsonResponse(response, status = 400)
		except Exception as e:

			# Exception Occured
			response = {"message":str(e.args[0]), "data": {}}
			return JsonResponse(response, status = 500)

	def delete(self,request,university_id,*args,**kwargs):
		"""
		View for deletion of Universities.
		"""

		# Fetching university object by id
		try:
			university = University.objects.get(id = university_id , isDelete = False)
		except:
			response = {"message":"Invalid University Id", "data": {}}
			return JsonResponse(response,status = 400)

		# Soft Deletion of university object
		university.isDelete = True
		university.save()

		response = {'message':"University Deleted",'data' : {}}
		return JsonResponse(response,status=200)

class CountryList(generics.ListAPIView):
	"""
	View for listing of Countries.
	"""

	def list(self,request,*args,**kwargs):
		"""
		View for Listing of Countries.
		"""

		# List of Countries
		country_data = [{"code":code,"name":name} for code,name in list(countries)]
		
		response = {"message":"Countries Listed", "data": country_data}
		return JsonResponse(response, status = 200)


class UniversitySearch(BaseDocumentViewSet):
	"""The University Search view."""

	# Specify Documemt,Serializer,Lookup field and Filter backends
	document = UniversityDocument
	serializer_class = UniversityDocumentSerializer
	lookup_field = 'id'
	filter_backends = [
		FilteringFilterBackend,
		OrderingFilterBackend,
		DefaultOrderingFilterBackend,
	]

	# Define filtering fields and Partial Search/Full Search fields
	filter_fields = {
	'domain': {
		'field': 'domain.raw',
		'lookups': [
			LOOKUP_QUERY_ENDSWITH,
		],
	},
	'country': 'country.code.raw',

	# Partial Search/Full Search by name
	'name': {
		'field': 'name.raw',
		'lookups': [
			LOOKUP_QUERY_CONTAINS,
		],
	},
	}

	# Define ordering fields
	ordering_fields = {
		'createdAt': 'createdAt',
		'name': 'name.raw',
	}

	# Specify default ordering
	ordering = ('-createdAt',)

	# Specify Pagination Class
	pagination_class = StandardResultsSetPagination

	# Specify Queryset
	def get_queryset(self):

		queryset = self.search.query()
		queryset.model = self.document.Django.model
		queryset = queryset.filter('term', isDelete=False)
		return queryset

	def list(self,request,*args,**kwargs):
		"""
		View for Searching and Filtering of Universities with Pagination.
		"""

		# Filtering the Queryset by filter Backends
		queryset = self.filter_queryset(self.get_queryset())

		# Paginating the Filtered queryset
		try:
			page = self.paginate_queryset(queryset)
		except:
			data = []
		else:
			if page is not None:
				# Serialized data for a single page
				data = self.get_serializer(page, many=True).data
			else:
				# Serialized data for queryset
				data = self.get_serializer(queryset, many=True).data

		if data:
			message = "Universities Listed"
		else:
			message = "No data available"

		response = {'message':message,'data' : data}
		return JsonResponse(response,status=200)