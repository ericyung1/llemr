from rest_framework import serializers
from osler.demographics import models

class DemographicsSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Demographics
        exclude = []