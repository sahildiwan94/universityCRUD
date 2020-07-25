from .models import University
import django_filters

class UniversityFilter(django_filters.FilterSet):
    """
    Customized filter for country code and end of the domain.
    """

    domain = django_filters.CharFilter(field_name="domain", lookup_expr='iendswith')
    country = django_filters.CharFilter(field_name="country", lookup_expr='iexact')

    class Meta:
    	
        model = University
        fields = ['country','domain']