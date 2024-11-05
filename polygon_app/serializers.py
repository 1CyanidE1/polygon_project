from rest_framework import serializers

from polygon_app.models import PolygonModel


class PolygonSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolygonModel
        fields = ['id', 'name', 'polygon', 'crosses_antimeridian']