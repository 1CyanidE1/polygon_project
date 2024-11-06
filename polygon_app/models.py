from django.contrib.gis.db import models
from django.contrib.gis.geos import Polygon
import logging


logger = logging.getLogger(__name__)


class PolygonModel(models.Model):
    name = models.CharField(max_length=200)
    polygon = models.PolygonField(srid=4326)
    crosses_antimeridian = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        coords = self.polygon.coords[0]
        logger.debug(f"Original coordinates: {coords}")
        self.crosses_antimeridian = False

        for i in range(len(coords) - 1):
            lon1 = coords[i][0]
            lon2 = coords[i + 1][0]

            logger.debug(f"Checking segment {i}: lon1={lon1}, lon2={lon2}, diff={abs(lon2 - lon1)}")

            if (lon1 < -90 and lon2 > 90) or (lon1 > 90 and lon2 < -90):
                self.crosses_antimeridian = True
                logger.debug(f"Antimeridian crossing detected at segment {i}")

                new_coords = []
                for coord in coords:
                    lon = coord[0]
                    lat = coord[1]

                    while lon > 180:
                        lon -= 360
                    while lon < -180:
                        lon += 360

                    new_coords.append((lon, lat))
                    logger.debug(f"Normalized coordinate: ({lon}, {lat})")

                self.polygon = Polygon(new_coords)
                break

        longitudes = [coord[0] for coord in coords]
        min_lon = min(longitudes)
        max_lon = max(longitudes)

        if max_lon - min_lon > 180:
            self.crosses_antimeridian = True
            logger.debug(f"Antimeridian crossing detected by longitude span: min={min_lon}, max={max_lon}")

        logger.debug(f"Final crosses_antimeridian value: {self.crosses_antimeridian}")
        logger.debug(f"Final coordinates: {self.polygon.coords[0]}")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
