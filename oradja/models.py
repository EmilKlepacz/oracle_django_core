from django.db import models

from oradja.utils.db_utils import next_sequence_value


# for tables already created in database set managed = False in Meta class.
# Django should not attempt to create, modify, or delete the table in the database.
# Django that it should not attempt to create, modify, or delete the table in the database.
# Use for ORM only!!!

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


# Placeholders only for foreign keys: matches the actual database table names
# NO NEED WHEN MODELS WILL NOT BE USED FULLY
class VmiLead(models.Model):
    class Meta:
        managed = False
        db_table = 'vmi_leads'


class ApiUser(models.Model):
    class Meta:
        managed = False
        db_table = 'api_users'


class VmiOrder(models.Model):
    class Meta:
        managed = False
        db_table = 'vmi_orders'


class UmvCustomer(models.Model):
    class Meta:
        managed = False
        db_table = 'umv_customers'


class VmiLeaConAddress(models.Model):
    class Meta:
        managed = False
        db_table = 'vmileacon_addresses'


class VmiTicket(models.Model):
    class Meta:
        managed = False
        db_table = 'vmi_tickets'


class UmvCusWalkSheet(models.Model):
    class Meta:
        managed = False
        db_table = 'umvcus_walksheets'


class UmvCusContact(models.Model):
    class Meta:
        managed = False
        db_table = 'umvcus_contacts'


class UmvCusCampaign(models.Model):
    class Meta:
        managed = False
        db_table = 'umvcus_campaign'


class UmvDocument(models.Model):
    umvdcm = models.BigIntegerField(db_column='umvdcm#',
                                    primary_key=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    umvdcmtem = models.BigIntegerField(db_column='umvdcmtem#', blank=True,
                                       null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    file_name = models.CharField(max_length=255, blank=True, null=True)
    file_data = models.BinaryField(blank=True, null=True)
    apiusr = models.ForeignKey('ApiUser', models.DO_NOTHING,
                               db_column='apiusr#')  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    created_dati = models.DateField()
    vmilea = models.ForeignKey('VmiLead', models.DO_NOTHING, db_column='vmilea#', blank=True,
                               null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    vmiord = models.ForeignKey('VmiOrder', models.DO_NOTHING, db_column='vmiord#', blank=True,
                               null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    umvcus = models.ForeignKey('UmvCustomer', models.DO_NOTHING, db_column='umvcus#', blank=True,
                               null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    umvpro = models.BigIntegerField(db_column='umvpro#', blank=True, null=True,
                                    db_comment='migrated umv project id')  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    vmileaconadr = models.ForeignKey('VmiLeaConAddress', models.DO_NOTHING, db_column='vmileaconadr#', blank=True,
                                     null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    internal = models.BooleanField(db_comment='0 - both internal and external;\n1 - internal only')
    notes = models.TextField(blank=True, null=True)
    apiusr = models.ForeignKey('ApiUser', models.DO_NOTHING, db_column='apiusr#updated',
                               related_name='umvdocument_apiusr_updated_set', blank=True,
                               null=True)  # Field renamed to remove unsuitable characters.
    updated_dati = models.DateField(blank=True, null=True)
    source_doc_id = models.BigIntegerField(blank=True, null=True,
                                           db_comment='migrated doc id: vmileadoc#, vmiorddoc#, vmiticdoc#')
    vmitic = models.ForeignKey('VmiTicket', models.DO_NOTHING, db_column='vmitic#', blank=True,
                               null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    umvdoccat = models.BigIntegerField(db_column='umvdoccat#', blank=True, null=True,
                                       db_comment='by COBRA')  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    umvcuswks = models.ForeignKey('UmvCusWalkSheet', models.DO_NOTHING, db_column='umvcuswks#', blank=True, null=True,
                                  db_comment='by COBRA')  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    umvcuscon = models.ForeignKey('UmvCusContact', models.DO_NOTHING, db_column='umvcuscon#', blank=True, null=True,
                                  db_comment='by COBRA')  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    expiry_date = models.DateField(blank=True, null=True, db_comment='by COBRA')
    umvcusdoc = models.BigIntegerField(db_column='umvcusdoc#', blank=True, null=True,
                                       db_comment='migrated cust doc id, by COBRA')  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    document_no = models.CharField(max_length=120, blank=True, null=True, db_comment='migrated cust doc no, by COBRA')
    signed_contract = models.BooleanField(blank=True, null=True)
    vmiordadr = models.BigIntegerField(db_column='vmiordadr#', blank=True,
                                       null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    sales_id = models.BigIntegerField(blank=True, null=True)
    file_format = models.IntegerField(blank=True, null=True)
    addition_type = models.CharField(max_length=50, blank=True, null=True)
    umvcuscam = models.ForeignKey('UmvCusCampaign', models.DO_NOTHING, db_column='umvcuscam#', blank=True,
                                  null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'umv_document'

    def save(self, *args, **kwargs):
        """
        Ensure that the primary key uses the database sequence.
        """
        if not self.umvdcm:
            self.umvdcm = next_sequence_value("umvdcm#s")
        super().save(*args, **kwargs)

    @classmethod
    def get_latest(cls, limit=100,
                   created_dati_from=None,
                   created_dati_to=None,
                   fetch_file_blob=False):

        columns = ["umvdcm", "file_name", "created_dati"]

        if fetch_file_blob:
            columns.append("file_data")

        queryset = cls.objects.all().values(*columns)

        if created_dati_from and created_dati_to:
            queryset = queryset.filter(created_dati__range=(created_dati_from, created_dati_to))
        elif created_dati_from:
            queryset = queryset.filter(created_dati__gte=created_dati_from)
        elif created_dati_to:
            queryset = queryset.filter(created_dati__lte=created_dati_to)

        return queryset.order_by("-created_dati")[:limit]
