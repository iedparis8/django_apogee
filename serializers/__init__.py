import django

from django_apogee.models import InsAdmEtp, InsAdmEtpInitial, Individu, Adresse

from rest_framework import serializers

class AdresseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adresse

class InsAdmEtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsAdmEtp

class InsAdmEtpInitialSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsAdmEtpInitial

class IndividuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Individu


# ############ A METTRE AILLEURS ?
# from duck_examen.models import RattachementCentreExamen
#
# class RattachementCentreExamenSerializer(serializers.ModelSerializer):
#     centre_label = serializers.SerializerMethodField()
#
#     class Meta:
#         model = RattachementCentreExamen
#
#     def get_centre_label(self, obj):
#         return obj.centre.label
#
#
# ## SPECIFIC AU DUCK_EXAMEN
#
# class DuckExamenSerializer(serializers.Serializer):
#     inscription = serializers.SerializerMethodField()
#     individu = serializers.SerializerMethodField()
#     adresse = serializers.SerializerMethodField()
#     rattachements = serializers.SerializerMethodField()
#
#     def get_inscription(self, obj):
#         return InsAdmEtpInitialSerializer(obj).data
#
#     def get_individu(self, obj):
#         return IndividuSerializer(obj.cod_ind, many=False).data
#
#     def get_adresse(self, obj):
#         try:
#             return str(Adresse.objects.get(cod_anu_ina=obj.cod_ind))
#
#         except:
#             try:
#                 return str(Adresse.objects.get(cod_ind=obj.cod_ind))
#
#             except:
#                 return None
#
#
#     def get_rattachements(self, obj):
#         def make_insadmetp_key_from_insadmetpinitial(inscription):
#             return ("{cod_anu}|{cod_ind}|{cod_etp}"
#                     "|{cod_vrs_vet}|{num_occ_iae}".format(cod_anu=inscription.cod_anu,
#                                                           cod_ind=inscription.cod_ind.cod_ind,
#                                                           cod_etp=inscription.cod_etp,
#                                                           cod_vrs_vet=inscription.cod_vrs_vet,
#                                                           num_occ_iae=inscription.num_occ_iae))
#
#         inscription_key = make_insadmetp_key_from_insadmetpinitial(obj)
#         try:
#             insadmetp = InsAdmEtp.objects.get(pk=inscription_key)
#
#         except django.core.exceptions.ObjectDoesNotExist:
#             return []
#
#         return RattachementCentreExamenSerializer(RattachementCentreExamen.objects.filter(inscription=insadmetp),
#                                                   many=True).data