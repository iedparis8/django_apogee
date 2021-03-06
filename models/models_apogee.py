# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django_apogee.managers import EtapeManager
from django_apogee.models.models_composite import CompositeInitial, CompositeImplementation
from django.utils.encoding import python_2_unicode_compatible
__author__ = 'paul'
import re
from django.db import models
"""
**L'accès aux tables d'apogée**

Contient toutes les tables de nomenclature.

"""

@python_2_unicode_compatible
class AnneeUni(models.Model):
    """Class d'accès pour la modification

    """
    cod_anu = models.CharField(u'Année', max_length=4, primary_key=True, db_column='COD_ANU')
    eta_anu_iae = models.CharField(u"Etat ouverture année", max_length=1, choices=(
        ('F', u"Fermé"),
        ('I', 'Inscription'),
        ('O', 'Ouvert')), default='I', db_column='ETA_ANU_IAE')

    def __str__(self):
        return str(self.cod_anu)

    class Meta:
        db_table = 'ANNEE_UNI'
        ordering = ['-cod_anu']
        app_label = 'django_apogee'


@python_2_unicode_compatible
class Pays(models.Model):
    cod_pay = models.CharField(max_length=3, primary_key=True, db_column='COD_PAY')
    cod_sis_pay = models.CharField(max_length=3, db_column='COD_SIS_PAY')
    lib_pay = models.CharField(max_length=50, db_column='LIB_PAY')
    lic_pay = models.CharField(max_length=20, db_column='LIC_PAY')
    lib_nat = models.CharField(max_length=50, db_column='LIB_NAT')
    tem_ouv_drt_sso_pay = models.CharField(max_length=1, db_column='TEM_OUV_DRT_SSO_PAY')
    tem_en_sve_pay = models.CharField(max_length=1, db_column='TEM_EN_SVE_PAY')
    tem_del = models.CharField(max_length=1, db_column='TEM_DEL')
    tem_afl_dec_ind_pay = models.CharField(max_length=1, db_column='TEM_AFL_DEC_IND_PAY')

    class Meta:
        db_table = u'PAYS'
        ordering = ['lic_pay']
        app_label = 'django_apogee'

    def __str__(self):
        return self.lib_pay


@python_2_unicode_compatible
class Departement(models.Model):
    cod_dep = models.CharField(max_length=3, primary_key=True, db_column='COD_DEP')
    cod_acd = models.IntegerField(db_column='COD_ACD')
    lib_dep = models.CharField(max_length=60, db_column='LIB_DEP')
    lic_dep = models.CharField(max_length=20, db_column='LIC_DEP')
    tem_en_sve_dep = models.CharField(max_length=1, db_column='TEM_EN_SVE_DEP')

    class Meta:
        db_table = u'DEPARTEMENT'
        ordering = ['lib_dep']
        app_label = 'django_apogee'

    def __str__(self):
        return self.lib_dep


@python_2_unicode_compatible
class SitFam(models.Model):
    """
    Les status familiales
    """
    cod_fam = models.CharField(max_length=1, primary_key=True, db_column='COD_FAM')
    cod_sis_fam = models.CharField(max_length=1, null=True, blank=True, db_column='COD_SIS_FAM')
    lib_fam = models.CharField(max_length=40, db_column='LIB_FAM')
    lic_fam = models.CharField(max_length=10, db_column='LIC_FAM')
    tem_en_sve_fam = models.CharField(max_length=1, choices=(('O', 'O'), ('N', 'N')),
                                      default='O', db_column='TEM_EN_SVE_FAM')
    
    def __str__(self):
        return self.lib_fam

    class Meta:
        db_table = u'SIT_FAM'
        app_label = 'django_apogee'


@python_2_unicode_compatible
class TypHandicap(models.Model):
    """Type d'handicap de l'étudiant
    """
    cod_thp = models.CharField(u"code type handicap", max_length=2,
                               primary_key=True, db_column='COD_THP')
    lib_thp = models.CharField(u"libelle long", max_length=50, db_column='LIB_THP')
    lic_thp = models.CharField(u"lielle court", max_length=20, db_column='LIC_THP')
    tem_tie_tps = models.CharField(u"temoin handicap permet tiers temps",
                                   max_length=1, choices=(('O', 'O'), ('N', 'N')), default='O', db_column='TEM_TIE_TPS')
    tem_en_sve_thp = models.CharField(u"temoin en service", max_length=1,
                                      choices=(('O', 'O'), ('N', 'N')), default='O', db_column='TEM_EN_SVE_THP')

    def __str__(self):
        return self.lib_thp

    class Meta:
        db_table = u"TYP_HANDICAP"
        app_label = 'django_apogee'


@python_2_unicode_compatible
class SitMil(models.Model):
    """Situation Militaire de l'étudiant
    """
    cod_sim = models.CharField(u"Code Situation militaire",
                               max_length=1, primary_key=True, db_column='COD_SIM')
    lib_sim = models.CharField(u"Libelle Long Situation Militaire",
                               max_length=50, db_column='LIB_SIM')
    lic_sim = models.CharField(u"lib court", max_length=20, db_column='LIC_SIM')
    tem_sai_dmm_lbt = models.CharField(
        u"temoin permettant une saisie coherente code situation militaire",
        max_length=1, choices=(('O', 'O'), ('N', 'N')), default='O', db_column='TEM_SAI_DMM_LBT')
    tem_en_sve_sim = models.CharField(u"temoin en service", max_length=1,
                                      choices=(('O', 'O'), ('N', 'N')), default='O', db_column='TEM_EN_SVE_SIM')
    tem_del_dip = models.CharField(u"Temoin de délivrance du diplome",
                                   max_length=1, choices=(('O', 'O'), ('N', 'N')), default='N', db_column='TEM_DEL_DIP')

    def __str__(self):
        return self.lib_sim

    class Meta:
        db_table = u"SIT_MIL"
        app_label = 'django_apogee'


@python_2_unicode_compatible
class ComBdiInitial(CompositeInitial):
    """Table permettant d'avoir une ville

    .. warning:: Vous ne devez jamais écrire dans cette table.
      il faut utiliser les données copiées dans ComBdi
    """
    cod_bdi = models.CharField(max_length=6, primary_key=True, db_column='COD_BDI')
    cod_com = models.CharField(max_length=6, db_column='COD_COM')
    lib_ach = models.CharField(max_length=26, db_column='LIB_ACH')
    eta_ptc_loc = models.CharField(max_length=3, db_column='ETA_PTC_LOC')
    eta_ptc_ach = models.CharField(max_length=3, db_column='ETA_PTC_ACH')
    tem_en_sve_cbd = models.CharField(max_length=3, db_column='TEM_EN_SVE_CBD')
    cod_fic_cbd = models.CharField(max_length=3, db_column='COD_FIC_CBD')

    _composite_field = ['cod_bdi', 'cod_com']

    def __str__(self):
        return "%s %s" % (self.cod_bdi, self.lib_ach)

    class Meta:
        db_table = 'COM_BDI'
        managed = False
        ordering = ['lib_ach']
        app_label = 'django_apogee'


@python_2_unicode_compatible
class ComBdi(CompositeImplementation):
    u"""
    **Classe de subtitution à ComBdiInitial**

    Lorsque django supportera les clé composites, migration de la table vers l'initiale
    """
    id = models.CharField(max_length=13, primary_key=True)
    cod_bdi = models.CharField(max_length=6, db_column='COD_BDI')
    cod_com = models.CharField(max_length=6, db_column='COD_COM')
    lib_ach = models.CharField(max_length=26, db_column='LIB_ACH')
    eta_ptc_loc = models.CharField(max_length=3, db_column='ETA_PTC_LOC')
    eta_ptc_ach = models.CharField(max_length=3, db_column='ETA_PTC_ACH')
    tem_en_sve_cbd = models.CharField(max_length=3, db_column='TEM_EN_SVE_CBD')
    cod_fic_cbd = models.CharField(max_length=3, db_column='COD_FIC_CBD')

    def __str__(self):
        return "%s %s" % (self.cod_bdi, self.lib_ach)

    class Meta:
        db_table = u'COM_BDI_COPY'
        ordering = ['lib_ach']
        app_label = 'django_apogee'


@python_2_unicode_compatible
class TypHebergement(models.Model):
    cod_thb = models.CharField(u"code type hébergement", max_length=1,
                               primary_key=True, db_column='COD_THB')
    lib_thb = models.CharField(u"libelle long type hébergement", max_length=60, db_column='LIB_THB')
    tem_en_sve_thb = models.CharField(u"temoin en service", max_length=1,
                                      default='O', choices=(('O', 'O'),
                                                            ('N', 'N')), db_column='TEM_EN_SVE_THB')

    def __str__(self):
        return self.lib_thb

    class Meta:
        db_table = u"TYP_HEBERGEMENT"
        app_label = 'django_apogee'


@python_2_unicode_compatible
class BacOuxEqu(models.Model):
    CHOICES = (
        ('O', 'O'),
        ('N', 'N'))
    cod_bac = models.CharField(
        u"Code Baccalaureat ou Equivalence",
        max_length=4, db_column=u'COD_BAC', primary_key=True)
    cod_sis_bac = models.CharField(
        u"Code SISE Baccalaureat ou Equivalence",
        max_length=4, db_column=u'COD_SIS_BAC')
    lib_bac = models.CharField(
        u"Libelle Long Baccalaureat ou Equivalence",
        max_length=80, db_column=u'LIB_BAC')
    lic_bac = models.CharField(u"Libelle Court Baccalaureat ou Equivalence",
                               max_length=20, db_column=u'LIC_BAC')
    tem_etb = models.CharField(
        u"Temoin Existence ou Suivi Etablissementd'Origine",
        max_length=1, choices=CHOICES, default=u'O', db_column=u'TEM_ETB')
    tem_mnb = models.CharField(
        u'Temoin Existence ou Suivi Mention Niveau Bac Obtenue',
        max_length=1, choices=CHOICES, default=u'O', db_column=u'TEM_MNB')
    tem_nat_bac = models.CharField(u'Temoin Nature de Bac',
                                   max_length=1, choices=CHOICES, default=u'O', db_column=u'TEM_NAT_BAC')
    tem_obt_tit_etb_sec = models.CharField(
        u'Temoin Preparation Bac Etablissement Secondaire',
        max_length=1, choices=CHOICES, default='O', db_column=u'TEM_OBT_TIT_ETB_SEC')
    tem_en_sve_bac = models.CharField(u'Temoin en Service',
                                      max_length=1, choices=CHOICES, default=u'O', db_column=u'TEM_EN_SVE_BAC')
    tem_deb = models.CharField(u'Temoin Departement du Bac',
                               max_length=1, choices=CHOICES, default=u'O', db_column=u'TEM_DEB')
    tem_del = models.CharField(u"Temoin d'Autorisation de Mise Hors Service",
                               max_length=1, choices=CHOICES, default=u'O', db_column=u'TEM_DEL')
    daa_deb_vld_bac = models.CharField(
        u"Annee de debut de periode de validite du baccalaureat",
        null=True, max_length=4, db_column=u'DAA_DEB_VLD_BAC')
    daa_fin_vld_bac = models.CharField(
        u'Annee de fin de periode de validite du baccalaureat',
        null=True, max_length=4, db_column=u'DAA_FIN_VLD_BAC')
    tem_type_equi = models.CharField(
        u'Temoin precisant si la serie de bac est une equivalence',
        max_length=1, choices=CHOICES, default=u'N', db_column=u'TEM_TYPE_EQUI')
    cod_sis = models.ForeignKey(u'SituationSise',
                                verbose_name=u"Code de la situation de l'annee precedente unique",
                                max_length=1, null=True, db_column=u'COD_SIS')
    cod_tds = models.CharField(u"Code du type de dernier diplome obtenu unique",
                               max_length=1, null=True, db_column=u'COD_TDS')

    def __str__(self):
        return re.sub(r'([0-9]{4}-)', '', self.lib_bac).title()

    class Meta:
        db_table = u'BAC_OUX_EQU'
        app_label = u'django_apogee'


@python_2_unicode_compatible
class MentionBac(models.Model):
    """Mention Bac
    """
    cod_mnb = models.CharField("code mention niveau bac", max_length=2,
                               primary_key=True, db_column='COD_MNB')
    lib_mnb = models.CharField("libelle long", max_length=50, db_column='LIB_MNB')
    lic_mnb = models.CharField("libelle court", max_length=20, db_column='LIC_MNB')
    tem_en_sve_mnb = models.CharField("temoin code en service", max_length=1,
                                      choices=(('O', 'O'), ('N', 'N')), default='O', db_column='TEM_EN_SVE_MNB')

    def __str__(self):
        return self.lib_mnb

    class Meta:
        db_table = "MENTION_NIV_BAC"
        app_label = 'django_apogee'


@python_2_unicode_compatible
class TypEtb(models.Model):
    """Type établissement
    """
    cod_tpe = models.CharField("code type etablissement",
                               max_length=2, primary_key=True, db_column='COD_TPE')
    cod_sis_tpe = models.CharField(
        "Correspondance Code SISE type établissement",
        max_length=2, null=True, db_column='COD_SIS_TPE')
    lib_tpe = models.CharField("libelle long", max_length=50, db_column='LIB_TPE')
    lic_tpe = models.CharField("libelle court", max_length=20, db_column='LIC_TPE')

    tem_det_tpe = models.CharField(
        "temoin detail possibl sur ce type d'etablissement", max_length=1,
        choices=(('O', 'O'), ('N', 'N')), default='O', db_column='TEM_DET_TPE')
    tem_en_sve_tpe = models.CharField("temoin code en service",
                                      max_length=1, choices=(('O', 'O'), ('N', 'N')), default='O',
                                      db_column='TEM_EN_SVE_TPE')
    tem_ges_trf_tpe = models.CharField("temoin gestion des transfert",
                                       max_length=1, choices=(('O', 'O'), ('N', 'N')), default='O',
                                       db_column='TEM_GES_TRF_TPE')
    tem_prop_autre_etb = models.CharField("temoin etablissement en cours",
                                          max_length=1, choices=(('O', 'O'), ('N', 'N')), default='N',
                                          db_column='TEM_PROP_AUTRE_ETB')

    class Meta:
        db_table = "TYP_ETB"
        app_label = 'django_apogee'

    def __str__(self):
        return self.lib_tpe


@python_2_unicode_compatible
class Etablissement(models.Model):
    cod_etb = models.CharField("code", max_length=8, primary_key=True, db_column='COD_ETB')
    cod_tpe = models.ForeignKey(TypEtb, db_column='COD_TPE')
    cod_dep = models.ForeignKey(Departement, db_column='COD_DEP')
    lib_etb = models.CharField("libelle long", max_length=50, db_column='LIB_ETB')
    cod_pos_adr_etb = models.CharField("Code postal", max_length=20, null=True, default=None,
                                       db_column='COD_POS_ADR_ETB')
    tem_en_sve_etb = models.CharField("temoin en service", max_length=1,
                                      default='O', choices=(('O', 'O'), ('N', 'N')),
                                      db_column='TEM_EN_SVE_ETB')
    tem_aut_sis_etb = models.CharField("temoin en service", max_length=1,
                                       default='O', choices=(('O', 'O'), ('N', 'N')),
                                       db_column='TEM_AUT_SIS_ETB')
    cod_aff_dep_etb = models.CharField("code", max_length=3, null=True,
                                       db_column='COD_AFF_DEP_ETB')
    cod_aff_etb = models.CharField("code", max_length=3, null=True,
                                   db_column='COD_AFF_ETB')

    lib_off_etb = models.CharField("libelle officiel", max_length=60, db_column='LIB_OFF_ETB')
    lib_art_off_etb = models.CharField(
        "article defini precedant le nom officiel",
        max_length=5, db_column='LIB_ART_OFF_ETB')
    cod_pay_adr_etb = models.ForeignKey(Pays, null=True, db_column='COD_PAY_ADR_ETB')

    def __str__(self):
        if self.cod_tpe_id == '10':
            return unicode(self.lib_etb)
        else:
            return self.lib_off_etb

    def get_type(self):
        if self.cod_pay_adr_etb and self.cod_pay_adr_etb.cod_pay != 100:
            return 'P'
        else:
            return 'D'

    def get_pays_dep(self):
        if self.cod_pay_adr_etb and self.cod_pay_adr_etb.cod_pay != 100:
            return self.cod_pay_adr_etb.cod_pay
        else:
            return self.cod_dep.cod_dep

    class Meta:
        db_table = u"ETABLISSEMENT"
        ordering = ['lib_etb']
        app_label = 'django_apogee'


@python_2_unicode_compatible
class CatSocPfl(models.Model):
    cod_pcs = models.CharField("code", max_length=2, primary_key=True, db_column='COD_PCS')
    lib_pcs = models.CharField("libelle long", max_length=50, db_column='LIB_PCS')
    tem_en_sve_pcs = models.CharField("temoin en service", max_length=1,
                                      default='O', choices=(('O', 'O'), ('N',
                                                                         'N')), db_column='TEM_EN_SVE_PCS')
    lib_web_pcs = models.CharField("libelle long", max_length=120, db_column='LIB_WEB_PCS')
    tem_sai_qtr = models.CharField("temoin en service", max_length=1,
                                   default='O', choices=(('O', 'O'), ('N',
                                                                      'N')), db_column='TEM_SAI_QTR')

    def __str__(self):
        return self.lib_web_pcs

    class Meta:
        db_table = "CAT_SOC_PFL"
        app_label = 'django_apogee'


@python_2_unicode_compatible
class QuotiteTra(models.Model):
    cod_qtr = models.CharField("code", max_length=1, primary_key=True, db_column='COD_QTR')
    lib_qtr = models.CharField("libelle long", max_length=50, db_column='LIB_QTR')
    lic_qtr = models.CharField("libelle court", max_length=50, db_column='LIC_QTR')
    lim1_qtr = models.CharField("libelle court", max_length=50, db_column='LIM1_QTR')
    lib_web_qtr = models.CharField("libelle court", max_length=120, db_column='LIB_WEB_QTR')
    tem_en_sve_qtr = models.CharField(
        "temoin en service",
        max_length=1,
        default='O',
        choices=(('O', 'O'), ('N', 'N')), db_column='TEM_EN_SVE_QTR')
    tem_cou_aut_reg_qtr = models.CharField(
        "couverture sécu",
        max_length=1,
        default='O',
        choices=(('O', 'O'), ('N', 'N')), db_column='TEM_COU_AUT_REG_QTR')

    def __str__(self):
        return self.lib_web_qtr

    class Meta:
        db_table = u"QUOTITE_TRA"
        app_label = 'django_apogee'


@python_2_unicode_compatible
class DomaineActPfl(models.Model):
    cod_dap = models.CharField(max_length=2, primary_key=True, db_column="COD_DAP")
    lib_web_dap = models.CharField(max_length=120, db_column="LIB_WEB_DAP", null=True)

    def __str__(self):
        return self.lib_web_dap

    class Meta:
        db_table = u"DOMAINE_ACT_PFL"
        app_label = "django_apogee"


@python_2_unicode_compatible
class SituationSise(models.Model):
    cod_sis = models.CharField("code", max_length=1, primary_key=True, db_column='COD_SIS')
    lib_sis = models.CharField("libelle long", max_length=130, db_column='LIB_SIS')
    tem_en_sve_sis = models.CharField(
        "temoin en service",
        max_length=1,
        default='O',
        choices=(('O', 'O'), ('N', 'N')), db_column='TEM_EN_SVE_SIS')

    def __str__(self):
        return self.lib_sis

    class Meta:
        db_table = u"SITUATION_SISE"
        app_label = 'django_apogee'


@python_2_unicode_compatible
class TypeDiplomeExt(models.Model):
    cod_tde = models.CharField("code", max_length=3, primary_key=True, db_column='COD_TDE')
    lib_web_tde = models.CharField("libelle long", max_length=130, db_column='LIB_WEB_TDE')
    lib_tde = models.CharField("libelle long", max_length=130, db_column='LIB_TDE')

    tem_en_sve_tde = models.CharField(
        "temoin en service",
        max_length=1,
        default='O',
        choices=(('O', 'O'), ('N', 'N')), db_column='TEM_EN_SVE_TDE')

    def __str__(self):
        return self.lib_tde

    class Meta:
        db_table = u"TYP_DIPLOME_EXT"
        app_label = 'django_apogee'


@python_2_unicode_compatible
class RegimeParent(models.Model):
    """**Régimes sécurité sociale des parents**

    :clé primaire: cod_rgp
    """
    cod_rgp = models.CharField(u"code régime des parents", max_length=2, primary_key=True, db_column="COD_RGP")
    lib_rgp = models.CharField(u"Libellé régime des parents", max_length=280, db_column="LIB_RGP")
    ordre_tri_rgp = models.CharField(u"Ordre de  de tri d'affichage", max_length=2, null=True,
                                     db_column="ORDRE_TRI_RGP")

    def __str__(self):
        return self.lib_rgp

    class Meta:
        db_table = "REGIME_PARENT"
        app_label = 'django_apogee'


@python_2_unicode_compatible
class MtfNonAflSso(models.Model):
    """
    **Motifs de non affiliation à la sécurité sociale**

    :clé primaire: cod_mns

    """
    cod_mns = models.CharField(u"Code motif non affiliation securite sociale", max_length=1, primary_key=True,
                               db_column="COD_MNS")
    lib_mns = models.CharField(u"Libelle long motif non affiliation", max_length=40, db_column="LIB_MNS")
    lic_mns = models.CharField(u"Libelle court motif non affiliation", max_length=10, db_column="LIC_MNS")
    tem_en_sve_mns = models.CharField(u"Temoin code en service", max_length=1, default='O',
                                      db_column="TEM_EN_SVE_MNS",
                                      choices=(('O', 'O'), ('N', 'N')))
    tem_del = models.CharField(u"Temoin d'autorisation de mise hors service", max_length=1, default='O',
                               choices=(('O', 'O'), ('N', 'N')),
                               db_column="TEM_DEL")

    def __str__(self):
        return self.lib_mns

    class Meta:
        db_table = 'MTF_NON_AFL_SSO'
        app_label = 'django_apogee'


@python_2_unicode_compatible
class SitSociale(models.Model):
    cod_soc = models.CharField("code situation sociale", max_length=2, primary_key=True, db_column='COD_SOC')
    lib_soc = models.CharField("libelle long", max_length=35, db_column='LIM1_SOC')
    lic_soc = models.CharField("libelle court", max_length=35, db_column='LIB_SOC')
    tem_en_sve_soc = models.CharField(u"Temoin code en service", max_length=1,
                                      choices=(('O', 'O'), ('N', 'N')),
                                      db_column="TEM_EN_SVE_SOC")
    tem_del = models.CharField(u"Témoin d'autorisation de mise hors service", max_length=1,
                               choices=(('O', 'O'), ('N', 'N')),
                               db_column="TEM_DEL")

    def __str__(self):
        return self.lib_soc

    class Meta:
        db_table = u'SIT_SOCIALE'
        app_label = 'django_apogee'


@python_2_unicode_compatible
class Bourse(models.Model):
    cod_brs = models.CharField("code situation sociale", max_length=2, primary_key=True, db_column='COD_BRS')
    cod_soc = models.ForeignKey(SitSociale, null=True, db_column='COD_SOC')
    lim1_brs = models.CharField("libelle long", max_length=35, db_column='LIM1_BRS')

    def __str__(self):
        return self.lim1_brs

    class Meta:
        db_table = u'BOURSE'
        app_label = 'django_apogee'


@python_2_unicode_compatible
class Composante(models.Model):
    """
    Composante de la fac
    """
    cod_cmp = models.CharField(u"code composante", max_length=3,
                               primary_key=True, db_column='COD_CMP')
    cod_tpc = models.CharField(u"code type composante", max_length=3, null=True,
                               db_column="COD_TPC",)
    lib_cmp = models.CharField(u"libelle", max_length=40, null=True,
                               db_column="LIB_CMP",)

    def __str__(self):
        return u"%s %s" % (self.cod_cmp, self.lib_cmp)

    class Meta:
        app_label = 'django_apogee'
        db_table = "COMPOSANTE"


@python_2_unicode_compatible
class CentreGestion(models.Model):
    """
    les centre de gestion : ceux sont les centres financiers à différencier des composantes.
    Une composante peut être un centre de gestion.
    """
    cod_cge = models.CharField(u"code centre de gestion", max_length=3, db_column="COD_CGE", primary_key=True)
    lib_cge = models.CharField(u"libellé", max_length=40, null=True, db_column="LIB_CGE")

    def __str__(self):
        return u"%s %s" % (self.cod_cge, self.lib_cge)

    class Meta:
        app_label = "django_apogee"
        db_table = "CENTRE_GESTION"


@python_2_unicode_compatible
class Etape(models.Model):
    cod_etp = models.CharField(u"Code etape", max_length=6, db_column="COD_ETP", primary_key=True, )
    cod_cyc = models.CharField(u"code sise", max_length=1, null=True, db_column="COD_CYC")
    cod_cur = models.CharField(u"cursus lmd", max_length=1, null=True, db_column="COD_CUR")
    lib_etp = models.CharField(u"label", max_length=60, null=True, db_column="LIB_ETP")
    objects = EtapeManager()

    def __str__(self):
        return u"%s" % self.lib_etp

    class Meta:
        app_label = 'django_apogee'
        verbose_name = "Etape d'un cursus"
        verbose_name_plural = "Etapes d'un cursus"
        db_table = "ETAPE"


@python_2_unicode_compatible
class EtpGererCge(models.Model):
    cod_etp = models.ForeignKey(Etape, verbose_name=u"code etape", db_column="COD_ETP", primary_key=True)
    cod_cge = models.ForeignKey(CentreGestion, verbose_name=u"code centre gestion",
                                db_column="COD_CGE", related_name="etape_centre_gestion",)
    cod_cmp = models.ForeignKey(Composante, verbose_name=u"code composante", db_column='COD_CMP')

    def __str__(self):
        return u"%s" % self.cod_etp

    class Meta:
        app_label = 'django_apogee'
        db_table = 'ETP_GERER_CGE'


@python_2_unicode_compatible
class Elp(models.Model):
    """
    Elément pedagogique
    """
    cod_elp = models.CharField(u"Code element pedagogique", max_length=8, primary_key=True, db_column="COD_ELP")
    cod_cmp = models.ForeignKey(Composante, verbose_name=u"code centre gestion",
                                db_column="COD_CMP", related_name="centre_gestion_elp",)
    lib_elp = models.CharField('libelle', max_length=120)
    eta_elp = models.CharField(u"etat", max_length=1, db_column="ETA_ELP")

    def __str__(self):
        return self.cod_elp

    class Meta:
        app_label = 'django_apogee'
        db_table = 'ELEMENT_PEDAGOGI'


@python_2_unicode_compatible
class ElpLibelleInitial(CompositeInitial):
    cod_elp = models.ForeignKey(Elp, primary_key=True, db_column='COD_ELP')
    cod_lng = models.CharField(u"Code langue", max_length=4, db_column="COD_LNG")
    lib_elp_lng = models.CharField(u"libelle", max_length=4000, null=True, db_column="LIB_ELP_LNG")
    _composite_field = ['cod_elp', 'cod_lng']

    def __str__(self):
        return self.lib_elp_lng

    class Meta:
        app_label = u'django_apogee'
        db_table = 'ELP_LIBELLE'


@python_2_unicode_compatible
class ElpLibelle(CompositeImplementation):
    id = models.CharField(max_length=13, primary_key=True)
    cod_elp = models.ForeignKey(Elp, db_column='COD_ELP')
    cod_lng = models.CharField(u"Code langue", max_length=4, db_column="COD_LNG", null=True)
    lib_elp_lng = models.CharField(u"libelle", max_length=4000, null=True, db_column="LIB_ELP_LNG")

    def __str__(self):
        return self.lib_elp_lng

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.id:
            self.id = str(self.cod_elp) + str(self.cod_lng)
        super(ElpLibelle, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        app_label = u'django_apogee'
        db_table = 'ELP_LIBELLE_COPY'

@python_2_unicode_compatible
class Diplome(models.Model):
    cod_dip = models.CharField('Code diplome', max_length=7, primary_key=True, db_column='COD_DIP')
    lib_dip = models.CharField(u"libelle diplome", max_length=60, db_column="LIB_DIP")

    def __str__(self):
        return self.lib_dip

    class Meta:
        app_label = 'django_apogee'
        db_table = 'DIPLOME'


@python_2_unicode_compatible
class CmpHabiliterVdiInitial(CompositeInitial):
    """Table composite
        utiliser CmpHabiliterVdi
    """

    cod_cmp = models.ForeignKey(Composante, primary_key=True, db_column='COD_CMP') 
    cod_dip = models.ForeignKey(Diplome, db_column="COD_DIP")
    cod_vrs_vdi = models.CharField(u"numero version diplome", max_length=3, db_column="COD_VRS_VDI")
    tem_en_sve_cvd = models.CharField(u"temoin en service", max_length=1, db_column="TEM_EN_SVE_CVD")
    _composite_field = ['cod_cmp', 'cod_dip', 'cod_vrs_vdi']

    def __str__(self):
        return self.cod_dip

    class Meta:
        managed = False
        app_label = 'django_apogee'
        db_table = 'CMP_HABILITER_VDI'


@python_2_unicode_compatible
class CmpHabiliterVdi(CompositeImplementation):
    """
    """
    id = models.CharField(max_length=17, primary_key=True)
    cod_cmp = models.ForeignKey(Composante, db_column='COD_CMP')
    cod_dip = models.ForeignKey(Diplome, db_column="COD_DIP")
    cod_vrs_vdi = models.CharField(u"numero version diplome", max_length=3, db_column="COD_VRS_VDI")
    tem_en_sve_cvd = models.CharField(u"temoin en service", max_length=1, db_column="TEM_EN_SVE_CVD", null=True)

    def __str__(self):
        return self.cod_dip.cod_dip

    class Meta:
        app_label = 'django_apogee'
        db_table = 'CMP_HABILITER_COPY'


@python_2_unicode_compatible
class SpecialiteVdi(models.Model):
    cod_svd = models.CharField(max_length=6, primary_key=True, db_column='COD_SVD')
    lib_svd = models.CharField(max_length=400, db_column='LIB_SVD')
    tem_en_sve_svd = models.CharField(u"", max_length=1, db_column="TEM_EN_SVE_SVD")

    def __str__(self):
        return self.lib_svd

    class Meta:
        app_label = 'django_apogee'
        db_table = 'SPECIALITE_VDI'


@python_2_unicode_compatible
class VersionDiplomeInitial(CompositeInitial):
    """
    :clé primaire composite: cod_dip + cod_vrs_vdi
    """
    cod_dip = models.ForeignKey(Diplome, verbose_name=u"code diplome", primary_key=True,
                                max_length=7, db_column="COD_DIP")
    cod_vrs_vdi = models.CharField(u"version diplome", max_length=3, db_column="COD_VRS_VDI")
    lic_vdi = models.CharField(u"libelle", max_length=25, db_column="LIC_VDI")
    cod_svd = models.ForeignKey(SpecialiteVdi, null=True, db_column="COD_SVD")

    _composite_field = ['cod_dip', 'cod_vrs_vdi']

    def __str__(self):
        return self.lic_vdi or ''

    class Meta:
        app_label = 'django_apogee'
        managed = False
        db_table = 'VERSION_DIPLOME'


@python_2_unicode_compatible
class VersionDiplome(CompositeImplementation):
    """
    :id: = cod_dip + cod_vrs_vdi
    """
    id = models.CharField('id', max_length=11, primary_key=True)
    cod_dip = models.ForeignKey(Diplome, verbose_name=u"code diplome", max_length=7, db_column="COD_DIP")
    cod_vrs_vdi = models.CharField(u"version diplome", max_length=3, db_column="COD_VRS_VDI")
    lic_vdi = models.CharField(u"libelle", max_length=25, db_column="LIC_VDI", null=True)
    cod_svd = models.ForeignKey(SpecialiteVdi, null=True, db_column="COD_SVD")

    def __str__(self):

        return self.lic_vdi or ''

    class Meta:
        app_label = 'django_apogee'
        db_table = 'VERSION_DIPLOME_COPY'


@python_2_unicode_compatible
class VersionEtapeInitial(CompositeInitial):
    """
    :clé primaire composite: cod_etp + cod_vrs_vet
    """
    cod_etp = models.CharField(u"code etape", max_length=6, primary_key=True, db_column="COD_ETP")
    cod_vrs_vet = models.CharField(u"version etape", max_length=3, db_column="COD_VRS_VET")

    _composite_field = ['cod_etp', 'cod_vrs_vet']

    def __str__(self):
        return self.cod_etp

    class Meta:
        managed = False
        app_label = 'django_apogee'
        db_table = 'VERSION_ETAPE'


@python_2_unicode_compatible
class VersionEtape(models.Model):
    """
    :id: = cod_etp + cod_vrs_vet
    """
    id = models.CharField('id', max_length=10, primary_key=True)
    cod_etp = models.CharField(u"code etape", max_length=6, db_column="COD_ETP")
    cod_vrs_vet = models.CharField(u"version etape", max_length=3, db_column="COD_VRS_VET")

    def __str__(self):
        return self.cod_etp

    class Meta:
        app_label = 'django_apogee'
        db_table = 'VERSION_ETAPE_COPY'


@python_2_unicode_compatible
class VdiFractionnerVetInitial(CompositeInitial):
    """
    Permet de récupérer les etapes pour une version de diplome.
    Pour l'instantant pas de foreignkey

    """
    cod_etp = models.CharField(u"code etape", max_length=6, primary_key=True, db_column="COD_ETP")
    cod_vrs_vet = models.CharField(u"version etape", max_length=3, db_column="COD_VRS_VET")
    cod_dip = models.CharField(u"code diplome", max_length=7, db_column="COD_DIP")
    cod_vrs_vdi = models.CharField(u"version diplome", max_length=3, db_column="COD_VRS_VDI")
    cod_sis_daa_min = models.CharField(u"Equivalent Annee Minimale de l'Etape pour un Diplome", max_length=2,
                                       null=True, db_column="COD_SIS_DAA_MIN")

    _composite_field = ['cod_etp', 'cod_vrs_vet', 'cod_dip', 'cod_vrs_vdi']

    def __str__(self):
        return self.cod_etp

    class Meta:
        managed = False
        app_label = 'django_apogee'
        db_table = 'VDI_FRACTIONNER_VET'


@python_2_unicode_compatible
class VdiFractionnerVet(CompositeImplementation):
    """
    Permet de récupérer les etapes pour une version de diplome.
    Pour l'instantant pas de foreignkey

    """
    id = models.CharField(u"id", max_length=22, primary_key=True)
    cod_etp = models.CharField(u"code etape", max_length=6, db_column="COD_ETP")
    cod_vrs_vet = models.CharField(u"version etape", max_length=3, db_column="COD_VRS_VET")
    cod_dip = models.CharField(u"code diplome", max_length=7, db_column="COD_DIP")
    cod_vrs_vdi = models.CharField(u"version diplome", max_length=3, db_column="COD_VRS_VDI")
    cod_sis_daa_min = models.CharField(u"Equivalent Annee Minimale de l'Etape pour un Diplome", max_length=2,
                                       null=True, db_column="COD_SIS_DAA_MIN")

    def __str__(self):
        return self.cod_etp

    class Meta:
        app_label = 'django_apogee'
        db_table = 'VDI_FRACTIONNER_VET_COPY'


