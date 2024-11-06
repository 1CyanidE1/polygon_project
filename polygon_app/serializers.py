from django.contrib.gis.geos import Polygon
from rest_framework import serializers

import logging

from polygon_app.models import PolygonModel


logger = logging.getLogger(__name__)


class PolygonSerializer(serializers.ModelSerializer):
    polygon = serializers.SerializerMethodField()

    class Meta:
        model = PolygonModel
        fields = ['id', 'name', 'polygon', 'crosses_antimeridian']

    def get_polygon(self, obj):
        """
        Converting polygon to GeoJSON format
        """
        if obj.polygon:
            coords = list(obj.polygon.coords[0])
            logger.debug(f"Converting to GeoJSON: {coords}")
            return {
                'type': 'Polygon',
                'coordinates': [coords]
            }
        return None

    def normalize_longitude(self, lon):
        """
        Normalizes longitude to range [-180, 180]
        """
        while lon > 180:
            lon -= 360
        while lon < -180:
            lon += 360
        return lon

    def validate_coordinates(self, coordinates):
        """
        Validating coordinates and normalizing them
        """
        if not coordinates or len(coordinates) < 3:
            raise serializers.ValidationError("Polygon must have at least 3 points")

        normalized_coordinates = []
        for lon, lat in coordinates:
            norm_lon = self.normalize_longitude(lon)
            if not (-90 <= lat <= 90):
                logger.warning(f"Invalid latitude value: {lat}")
                raise serializers.ValidationError(f"Latitude must be between -90 and 90, got {lat}")
            normalized_coordinates.append((norm_lon, lat))

        if normalized_coordinates[0] != normalized_coordinates[-1]:
            normalized_coordinates.append(normalized_coordinates[0])

        logger.debug(f"Normalized coordinates: {normalized_coordinates}")
        return normalized_coordinates

    def check_antimeridian(self, coordinates):
        """
        Checking antimeridian crossing
        """
        normalized_coords = [(self.normalize_longitude(lon), lat) for lon, lat in coordinates]

        for i in range(len(normalized_coords) - 1):
            lon1 = normalized_coords[i][0]
            lon2 = normalized_coords[i + 1][0]

            logger.debug(f"Checking segment {i}: lon1={lon1}, lon2={lon2}")

            if abs(lon2 - lon1) > 180:
                logger.info(f"Antimeridian crossing detected between points {i} and {i + 1}")
                return True

            if (lon1 < -90 and lon2 > 90) or (lon1 > 90 and lon2 < -90):
                logger.info(f"Antimeridian crossing detected between points {i} and {i + 1}")
                return True

        longitudes = [coord[0] for coord in normalized_coords]
        min_lon = min(longitudes)
        max_lon = max(longitudes)
        logger.debug(f"Longitude range: min={min_lon}, max={max_lon}")

        if max_lon - min_lon > 180:
            logger.info(f"Antimeridian crossing detected by longitude span")
            return True

        return False

    def create(self, validated_data):
        """
        Creating new object from GeoJSON data
        """
        polygon_data = self.initial_data.get('polygon')
        logger.debug(f"Received polygon data: {polygon_data}")

        if polygon_data and isinstance(polygon_data, dict):
            if polygon_data['type'] != 'Polygon':
                raise serializers.ValidationError("Invalid geometry type")

            coordinates = polygon_data['coordinates'][0]
            logger.debug(f"Extracted coordinates: {coordinates}")

            normalized_coordinates = self.validate_coordinates(coordinates)

            crosses_antimeridian = self.check_antimeridian(coordinates)
            logger.debug(f"Crosses antimeridian: {crosses_antimeridian}")

            polygon = Polygon(normalized_coordinates)
            validated_data['polygon'] = polygon
            validated_data['crosses_antimeridian'] = crosses_antimeridian

        instance = super().create(validated_data)
        logger.debug(f"Created polygon with id {instance.id}, crosses_antimeridian: {instance.crosses_antimeridian}")
        return instance

    def update(self, instance, validated_data):
        """
        Updating existing objects
        """
        polygon_data = self.initial_data.get('polygon')
        logger.debug(f"Updating polygon {instance.id} with data: {polygon_data}")

        if polygon_data and isinstance(polygon_data, dict):
            if polygon_data['type'] != 'Polygon':
                raise serializers.ValidationError("Invalid geometry type")

            coordinates = polygon_data['coordinates'][0]

            normalized_coordinates = self.validate_coordinates(coordinates)

            crosses_antimeridian = self.check_antimeridian(coordinates)
            logger.debug(f"Updated polygon crosses antimeridian: {crosses_antimeridian}")

            polygon = Polygon(normalized_coordinates)
            validated_data['polygon'] = polygon
            validated_data['crosses_antimeridian'] = crosses_antimeridian

        instance = super().update(instance, validated_data)
        logger.debug(f"Updated polygon {instance.id}, crosses_antimeridian: {instance.crosses_antimeridian}")
        return instance
