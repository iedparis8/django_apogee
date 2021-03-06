# -*- coding: utf-8 -*-
from django.conf import settings
from django_apogee.models import AnneeUni, VersionEtape as VersionEtapeApogee, EtpGererCge, Etape, ConfAnneeUni
from duck_inscription.models import SettingAnneeUni, SettingsEtape, Wish

__author__ = 'paul'
from django.core.management.base import BaseCommand
APOGEE_CONNECTION = getattr(settings, 'APOGEE_CONNECTION', 'oracle')


class Command(BaseCommand):
    def handle(self, *args, **options):
        #on récupére les personnes du jour (soit la date de création, de modif plus grand que la veille
        print u"debut d'initialisation"
        print u"création de settings pour les années universitaires"
        for annee in AnneeUni.objects.all():
            ConfAnneeUni.objects.get_or_create(cod_anu=annee.cod_anu, anneeuni_ptr=annee)
        print u"création des étapes"

        print "fin initialisation"






