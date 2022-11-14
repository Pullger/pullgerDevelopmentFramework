from django.db import models
from django.db.models import signals
from django.dispatch import receiver


class DomainsManager(models.Manager):
    pass


class Domains(models.Model):
    uuid = models.CharField(max_length=36, primary_key=True)
    url = models.CharField(max_length=300, null=False)
    description = models.CharField(max_length=300, null=False)

    # id = models.IntegerField(blank=False, null=True)
    # nick = models.CharField(max_length=150, null=True)
    #
    # first_name = models.CharField(max_length=150, null=True)
    # second_name = models.CharField(max_length=150, null=True)
    # full_name = models.CharField(max_length=300, null=True)
    #
    # url = models.CharField(max_length=300, null=True)
    # discription = models.CharField(max_length=300, null=True)
    #
    # location = models.CharField(max_length=300, null=True)
    #
    # date_small_loaded = models.DateField(null=True)
    # date_full_loaded = models.DateField(null=True)


@receiver(signals.pre_save, sender=Domains)
def add_domain_uuid(sender, instance, **kwargs):
    import uuid

    if not instance.uuid:
        instance.uuid = str(uuid.uuid1())
