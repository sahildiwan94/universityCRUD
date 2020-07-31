from rest_framework import serializers
from .models import University
import dateutil.parser
from datetime import time
from .documents import UniversityDocument
import validators
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer


class UniversitySerializer(serializers.ModelSerializer):
	"""
	Model Serializer for University
	"""

	# Model,Serializer fields,Serializer fields validation
	class Meta:

		model = University
		fields = ('id','name','domain','web_page','country','createdAt')
		extra_kwargs = {
		"name":{"allow_blank":False,"error_messages":{"invalid":"Invalid name","required":"name field is required",
		"max_length":"name can be of max 150 characters","blank":"name cannot be blank"}},
		"domain":{"allow_blank":False,"error_messages":{"invalid":"Invalid domain","required":"domain field is required",
		"max_length":"domain can be of max 100 characters","blank":"domain cannot be blank"}},
		"country":{"allow_blank":False,"error_messages":{"invalid_choice":"Invalid country","required":"country field is required",
		"max_length":"country can be of max 100 characters","blank":"country cannot be blank"}},
		"web_page":{"allow_blank":False,"error_messages":{"invalid":"Invalid web_page","required":"web_page field is required",
		"max_length":"web_page can be of max 100 characters","blank":"web_page cannot be blank"}},
		}

	# Validity of Domain Field
	def validate_domain(self,value):
		domain = validators.domain(value)
		if domain != True:
			raise serializers.ValidationError("Invalid Domain")
		return value

	# Representation of serialized data
	def to_representation(self, instance):

		obj = super().to_representation(instance)

		obj['createdAt'] = str(dateutil.parser.parse(obj['createdAt']).date()) + " " + time.strftime(dateutil.parser.parse(obj['createdAt']).time(),"%H:%M")
		obj['alpha_two_code'] = obj['country']
		obj['country'] = instance.country.name

		return obj

	# Creation of university object
	def create(self,validated_data):

		university = University.objects.create(**validated_data)

		return university

	# Updation of university object
	def update(self,instance,validated_data):

		instance.name = validated_data.get("name")
		instance.domain = validated_data.get("domain")
		instance.country = validated_data.get("country")
		instance.web_page = validated_data.get("web_page")

		instance.save()

		return instance


class UniversityDocumentSerializer(DocumentSerializer):
	"""Serializer for University document."""

	class Meta(object):
		"""Meta options."""
		document = UniversityDocument
		fields = ('id','name','domain','web_page','country','createdAt')

	# Representation of serialized data
	def to_representation(self, instance):

		obj = super().to_representation(instance)

		obj['createdAt'] = str(dateutil.parser.parse(obj['createdAt']).date()) + " " + time.strftime(dateutil.parser.parse(obj['createdAt']).time(),"%H:%M")
		obj['alpha_two_code'] = instance.country.code
		obj['country'] = instance.country.name

		return obj