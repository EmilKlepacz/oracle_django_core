import re
from datetime import date
from typing import Optional, List

from django.db import models
from django.db.models import QuerySet

from oradja.file_manager.file_type import FileType
from oradja.utils.db_utils import next_sequence_value


# for tables already created in database set managed = False in Meta class.
# Django should not attempt to create, modify, or delete the table in the database.
# Django that it should not attempt to create, modify, or delete the table in the database.
# Use for ORM only!!!

# Placeholders only for foreign keys: matches the actual database table names
# NO NEED AS MODELS WILL NOT BE USED FULLY

######## BEGIN: models not complete, use for placeholder for fk in other tables########
class VmiLead(models.Model):
    vmilea = models.BigIntegerField(db_column='vmilea#',
                                    primary_key=True)

    class Meta:
        managed = False
        db_table = 'vmi_leads'


class VmiOrder(models.Model):
    vmiord = models.BigIntegerField(db_column='vmiord#',
                                    primary_key=True)

    class Meta:
        managed = False
        db_table = 'vmi_orders'


class UmvCustomer(models.Model):
    umvcus = models.BigIntegerField(db_column='umvcus#',
                                    primary_key=True)

    class Meta:
        managed = False
        db_table = 'umv_customers'


class VmiLeaConAddress(models.Model):
    vmileaconadr = models.BigIntegerField(db_column='vmileaconadr#',
                                          primary_key=True)

    class Meta:
        managed = False
        db_table = 'vmileacon_addresses'


class VmiTicket(models.Model):
    vmitic = models.BigIntegerField(db_column='vmitic#',
                                    primary_key=True)

    class Meta:
        managed = False
        db_table = 'vmi_tickets'


class UmvCusWalkSheet(models.Model):
    umvcuswks = models.BigIntegerField(db_column='umvcuswks#',
                                       primary_key=True)

    class Meta:
        managed = False
        db_table = 'umvcus_walksheets'


class UmvCusContact(models.Model):
    umvcuscon = models.BigIntegerField(db_column='umvcuscon#',
                                       primary_key=True)

    class Meta:
        managed = False
        db_table = 'umvcus_contacts'


class UmvCusCampaign(models.Model):
    umvcuscam = models.BigIntegerField(db_column='umvcuscam#',
                                       primary_key=True)

    class Meta:
        managed = False
        db_table = 'umvcus_campaign'


class ApiDomain(models.Model):
    apidom = models.BigIntegerField(db_column='apidomd#',
                                    primary_key=True)

    class Meta:
        managed = False
        db_table = 'umvcus_campaign'


######## END: models not complete, use for placeholder for fk in other tables########


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


class ApiUser(models.Model):
    apiusr = models.IntegerField(db_column='apiusr#', primary_key=True)
    created_dati = models.DateField()
    name = models.CharField(max_length=64)
    password = models.CharField(max_length=160, blank=True, null=True)
    pass_chg_dati = models.DateField(blank=True, null=True)
    pass_expired = models.BooleanField(db_comment='0 - no, 1 - yes')
    locked = models.BooleanField(db_comment='0 - no, 1 - yes')
    effective_dati = models.DateField(blank=True, null=True)
    expiry_dati = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=256, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    first_name = models.CharField(max_length=64, blank=True, null=True)
    phone_1 = models.CharField(max_length=4000, blank=True, null=True)
    phone_2 = models.CharField(max_length=60, blank=True, null=True)
    note = models.CharField(max_length=2000, blank=True, null=True)
    authentication = models.BooleanField(db_comment='1 - standard; 2 - domain; 3 - both')
    authorization = models.BooleanField(db_comment='1 - standard; 2 - domain; 3 - both')
    pass_autoexp_days = models.IntegerField(blank=True, null=True,
                                            db_comment='null - system default; 0 - never; n - in n days')
    apiusr_by = models.ForeignKey('self', models.DO_NOTHING, db_column='apiusr#by')
    label = models.CharField(max_length=60, blank=True, null=True, db_comment='display label if user is not a person')
    user_type = models.BooleanField(db_comment='1 - person; 2 - system')
    apidom = models.ForeignKey('ApiDomain', models.DO_NOTHING, db_column='apidom#', blank=True, null=True,
                               db_comment='null - internal user')
    auth_fail_count = models.IntegerField(blank=True, null=True)
    auth_lock_dati = models.DateField(blank=True, null=True)
    keep_login_log = models.BooleanField(blank=True, null=True)
    tf_type = models.BooleanField(blank=True, null=True,
                                  db_comment='null: login without 2-Factor-Authentication / 1: 2-F-A via SMS / 2: 2-F-A via email')
    tf_mobile = models.CharField(max_length=256, blank=True, null=True)
    tf_email = models.CharField(max_length=256, blank=True, null=True)
    last_login_dati = models.DateField(blank=True, null=True)
    is_anonymized = models.BooleanField()
    is_password_reset = models.BooleanField(blank=True, null=True)
    password_reset_dati = models.DateField(blank=True, null=True)
    ngum_user_id = models.CharField(max_length=256, blank=True, null=True)
    ngum_locked_dati = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'api_users'
        unique_together = (('name', 'apidom'),)


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
    apiusr_updated = models.ForeignKey('ApiUser', models.DO_NOTHING, db_column='apiusr#updated', blank=True,
                                       null=True,
                                       related_name='umvdocument_apiusr_updated_set')  # Field renamed to remove unsuitable characters.
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
    def query_docs(cls,
                   limit: int = 100,
                   created_dati_from: Optional[date] = None,
                   created_dati_to: Optional[date] = None,
                   fetch_file_blob: bool = False,
                   ids: Optional[List[int]] = None,  # when id list is not empty then query by ids
                   file_types: Optional[List[FileType]] = None,
                   **kwargs) -> QuerySet:

        columns = ["umvdcm", "file_name", "created_dati"]

        if fetch_file_blob:
            columns.append("file_data")

        queryset = cls.objects.all().exclude(file_data__isnull=True).values(*columns)

        if ids:
            queryset = queryset.filter(umvdcm__in=ids)
        else:
            if created_dati_from and created_dati_to:
                queryset = queryset.filter(created_dati__range=(created_dati_from, created_dati_to))
            elif created_dati_from:
                queryset = queryset.filter(created_dati__gte=created_dati_from)
            elif created_dati_to:
                queryset = queryset.filter(created_dati__lte=created_dati_to)

        if file_types:
            file_type_values = [file_type.value for file_type in file_types]
            queryset = queryset.filter(file_name__iregex=r"\.({})$".format('|'.join(file_type_values)))

        return queryset.order_by("-created_dati")[:limit]
