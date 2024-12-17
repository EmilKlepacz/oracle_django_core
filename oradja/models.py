from django.db import models


class ApiModProperty(models.Model):
    apimodpro = models.IntegerField(db_column='apimodpro#',
                                    primary_key=True)
    apimod = models.ForeignKey('ApiModule', on_delete=models.CASCADE,
                               db_column='apimod#')
    name = models.CharField(max_length=30)
    value = models.CharField(max_length=2000, blank=True, null=True)
    default_value = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'apimod_properties'


# for tables already created in database set managed = False in Meta class.
# Django should not attempt to create, modify, or delete the table in the database.
# Django that it should not attempt to create, modify, or delete the table in the database.
# Use for ORM only!!!
class ApiModule(models.Model):
    apimod = models.IntegerField(db_column='apimod#',
                                 primary_key=True)
    name = models.CharField(max_length=20)
    id = models.CharField(max_length=3)
    path = models.CharField(max_length=15, blank=True, null=True, db_comment='Should be read as: "parent module path"')
    module_type = models.BooleanField(db_comment='1 - standard; 2 - table')
    short_desc = models.CharField(max_length=120, blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    apimod_parent = models.ForeignKey('self', on_delete=models.CASCADE, db_column='apimod#parent', blank=True,
                                      null=True)
    registration_dati = models.DateField(blank=True, null=True)
    monitor_level = models.BooleanField(blank=True, null=True,
                                        db_comment='1 - none; 2 - statistics; 3 - calls; 4 - parameters')

    class Meta:
        managed = False
        db_table = 'api_modules'
        unique_together = (('path', 'id'), ('path', 'name'),)
