from django.db import models
from django_countries.fields import CountryField


class BaseModel(models.Model):
    """
    Abstract Base Model which is inherited by all models.
    """
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    isActive = models.BooleanField(default = True)
    isDelete = models.BooleanField(default = False)

    class Meta:
       abstract = True


class University(BaseModel):
    """
    Model for University.
    All fields are required.
    """
    name = models.CharField(max_length=150)
    domain = models.CharField(max_length=100)
    web_page = models.URLField()
    country = CountryField()

    class Meta:
        verbose_name = "University"
        verbose_name_plural = "Universities"
        db_table = "university"

    def __str__(self):
        return self.name
