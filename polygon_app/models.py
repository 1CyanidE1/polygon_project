from django.contrib.gis.db import models
from django.contrib.gis.geos import Polygon


class PolygonModel(models.Model):
    name = models.CharField(max_length=200)
    polygon = models.PolygonField(srid=4326)
    crosses_antimeridian = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        coords = self.polygon.coords[0]
        for i in range(len(coords) - 1):
            lon1 = coords[i][0]
            lon2 = coords[i + 1][0]

            if abs(lon1 - lon2) > 180:
                self.crosses_antimeridian = True

                new_coords = []
                for coord in coords:
                    lon = coord[0]
                    lat = coord[1]
                    if lon > 180:
                        lon = lon - 360
                    new_coords.append((lon, lat))

                self.polygon = Polygon(new_coords)
                break

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
