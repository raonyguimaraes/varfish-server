"""Factory Boy factory classes for ``variants``."""
import uuid

import factory
from django.utils import timezone

from projectroles.models import SODAR_CONSTANTS

from annotation.tests.factories import AnnotationFactory
from bgjobs.tests.factories import BackgroundJobFactory
from clinvar.tests.factories import ResubmitClinvarFormDataFactory
from ..models import (
    Case,
    SmallVariant,
    SmallVariantQuery,
    ProjectCasesSmallVariantQuery,
    SmallVariantSummary,
    ClinvarQuery,
    FilterBgJob,
    ProjectCasesFilterBgJob,
    CaseAwareProject,
    ClinvarBgJob,
    DistillerSubmissionBgJob,
    ExportFileBgJob,
    ExportFileJobResult,
    ExportProjectCasesFileBgJob,
    ExportProjectCasesFileBgJobResult,
    SmallVariantFlags,
    SmallVariantComment,
)
import typing
import attr


@attr.s(auto_attribs=True)
class FormDataFactoryBase:
    database_select: str = "refseq"
    var_type_snv: bool = True
    var_type_mnv: bool = True
    var_type_indel: bool = True
    exac_enabled: bool = False
    exac_frequency: float = 0.0
    exac_heterozygous: int = 0
    exac_homozygous: int = 0
    thousand_genomes_enabled: bool = False
    thousand_genomes_frequency: float = 0.0
    thousand_genomes_heterozygous: int = 0
    thousand_genomes_homozygous: int = 0
    gnomad_exomes_enabled: bool = False
    gnomad_exomes_frequency: float = 0.0
    gnomad_exomes_heterozygous: int = 0
    gnomad_exomes_homozygous: int = 0
    gnomad_genomes_enabled: bool = False
    gnomad_genomes_frequency: float = 0.0
    gnomad_genomes_heterozygous: int = 0
    gnomad_genomes_homozygous: int = 0
    inhouse_enabled: bool = False
    inhouse_carriers: int = 0
    inhouse_heterozygous: int = 0
    inhouse_homozygous: int = 0
    transcripts_coding: bool = True
    transcripts_noncoding: bool = True
    require_in_clinvar: bool = False
    remove_if_in_dbsnp: bool = False
    require_in_hgmd_public: bool = False
    display_hgmd_public_membership: bool = False
    clinvar_include_benign: bool = False
    clinvar_include_likely_benign: bool = False
    clinvar_include_uncertain_significance: bool = False
    clinvar_include_likely_pathogenic: bool = True
    clinvar_include_pathogenic: bool = True

    # This is a dummy attribute to generate the name-dependent fields.
    # It is removed after initialization.
    names: typing.List[str] = []

    def __attrs_post_init__(self):
        for name in self.names:
            self.__dict__.update(
                {
                    "%s_fail" % name: "ignore",
                    "%s_gt" % name: "any",
                    "%s_dp_het" % name: 0,
                    "%s_dp_hom" % name: 0,
                    "%s_ab" % name: 0,
                    "%s_gq" % name: 0,
                    "%s_ad" % name: 0,
                }
            )
        delattr(self, "names")


@attr.s(auto_attribs=True)
class ProcessedFormDataFactory(FormDataFactoryBase):
    """Factory for the filter form data after cleaning.

    The genotype filters are missing as they are added when running the test to fetch the current patient name that is
    unknown up to then. Same holds true for the case sodar_uuid.
    """

    effects: typing.List[str] = attr.Factory(lambda: list(["synonymous_variant"]))
    gene_blacklist: typing.List[str] = attr.Factory(list)
    genomic_region: typing.List[str] = attr.Factory(list)
    gene_whitelist: typing.List[str] = attr.Factory(list)


@attr.s(auto_attribs=True)
class ResubmitFormDataFactory(ProcessedFormDataFactory):
    result_rows_limit: int = 80
    submit: str = "display"
    file_type: str = "tsv"
    export_flags: bool = True
    export_comments: bool = True

    def __attrs_post_init__(self):
        for name in self.names:
            self.__dict__.update({"%s_export" % name: True})
        super().__attrs_post_init__()


@attr.s(auto_attribs=True)
class FormDataFactory(FormDataFactoryBase):
    """Factory for the data transferred from the filter form."""

    compound_recessive_enabled: bool = False
    effect_coding_transcript_intron_variant: bool = True
    effect_complex_substitution: bool = True
    effect_direct_tandem_duplication: bool = True
    effect_disruptive_inframe_deletion: bool = True
    effect_disruptive_inframe_insertion: bool = True
    effect_downstream_gene_variant: bool = True
    effect_exon_loss_variant: bool = True
    effect_feature_truncation: bool = True
    effect_five_prime_UTR_exon_variant: bool = True
    effect_five_prime_UTR_intron_variant: bool = True
    effect_frameshift_elongation: bool = True
    effect_frameshift_truncation: bool = True
    effect_frameshift_variant: bool = True
    effect_inframe_deletion: bool = True
    effect_inframe_insertion: bool = True
    effect_intergenic_variant: bool = True
    effect_internal_feature_elongation: bool = True
    effect_missense_variant: bool = True
    effect_mnv: bool = True
    effect_non_coding_transcript_exon_variant: bool = True
    effect_non_coding_transcript_intron_variant: bool = True
    effect_splice_acceptor_variant: bool = True
    effect_splice_donor_variant: bool = True
    effect_splice_region_variant: bool = True
    effect_start_lost: bool = True
    effect_stop_gained: bool = True
    effect_stop_lost: bool = True
    effect_stop_retained_variant: bool = True
    effect_structural_variant: bool = True
    effect_synonymous_variant: bool = True
    effect_three_prime_UTR_exon_variant: bool = True
    effect_three_prime_UTR_intron_variant: bool = True
    effect_transcript_ablation: bool = True
    effect_upstream_gene_variant: bool = True
    gene_blacklist: str = ""
    genomic_region: str = ""
    gene_whitelist: str = ""
    flag_bookmarked: bool = True
    flag_candidate: bool = True
    flag_final_causative: bool = True
    flag_for_validation: bool = True
    flag_phenotype_match_empty: bool = True
    flag_phenotype_match_negative: bool = True
    flag_phenotype_match_positive: bool = True
    flag_phenotype_match_uncertain: bool = True
    flag_simple_empty: bool = True
    flag_summary_empty: bool = True
    flag_summary_negative: bool = True
    flag_summary_positive: bool = True
    flag_summary_uncertain: bool = True
    flag_validation_empty: bool = True
    flag_validation_negative: bool = True
    flag_validation_positive: bool = True
    flag_validation_uncertain: bool = True
    flag_visual_empty: bool = True
    flag_visual_negative: bool = True
    flag_visual_positive: bool = True
    flag_visual_uncertain: bool = True
    prio_enabled: bool = False
    prio_algorithm: str = ""
    prio_hpo_terms: typing.List[str] = []
    patho_enabled: bool = False
    patho_score: str = ""
    file_type: str = "tsv"
    export_flags: bool = True
    export_comments: bool = True
    result_rows_limit: int = 80
    training_mode: bool = False
    submit: str = "display"
    filter_job_uuid: uuid.UUID = None
    # This is a dummy attribute to generate the name-dependent fields.
    # It is removed after initialization.
    names: typing.List[str] = []

    def __attrs_post_init__(self):
        for name in self.names:
            self.__dict__.update({"%s_export" % name: True})
        super().__attrs_post_init__()


@attr.s(auto_attribs=True)
class ChromosomalPositionFormDataFactoryBase:
    release: str = "GRCh37"
    chromosome: str = None
    position: int = None
    reference: str = None
    alternative: str = None


@attr.s(auto_attribs=True)
class SmallVariantFlagsFormDataFactory(ChromosomalPositionFormDataFactoryBase):
    flag_bookmarked: bool = True
    flag_candidate: bool = False
    flag_final_causative: bool = False
    flag_for_validation: bool = False
    flag_visual: str = "empty"
    flag_validation: str = "empty"
    flag_phenotype_match: str = "empty"
    flag_summary: str = "empty"


@attr.s(auto_attribs=True)
class SmallVariantCommentFormDataFactory(ChromosomalPositionFormDataFactoryBase):
    text: str = "Comment X"


@attr.s(auto_attribs=True)
class AcmgCriteriaRatingFormDataFactory(ChromosomalPositionFormDataFactoryBase):
    pvs1: int = 0
    ps1: int = 0
    ps2: int = 0
    ps3: int = 0
    ps4: int = 0
    pm1: int = 0
    pm2: int = 0
    pm3: int = 0
    pm4: int = 0
    pm5: int = 0
    pm6: int = 0
    pp1: int = 0
    pp2: int = 0
    pp3: int = 0
    pp4: int = 0
    pp5: int = 0
    ba1: int = 0
    bs1: int = 0
    bs2: int = 0
    bs3: int = 0
    bs4: int = 0
    bp1: int = 0
    bp2: int = 0
    bp3: int = 0
    bp4: int = 0
    bp5: int = 0
    bp6: int = 0
    bp7: int = 0


class ProjectFactory(factory.django.DjangoModelFactory):
    """Factory for creating ``projectroles`` ``Project`` objects."""

    class Meta:
        model = CaseAwareProject

    title = factory.Sequence(lambda n: "Project %03d" % n)
    type = SODAR_CONSTANTS["PROJECT_TYPE_PROJECT"]
    parent = None
    description = factory.Sequence(lambda n: "This is project %03d" % n)


class CaseFactory(factory.django.DjangoModelFactory):
    """Factory for creating ``Case`` objects."""

    class Meta:
        model = Case

    class Params:
        #: The sex of the index
        sex = 1  # 1: unaffected, 2: affected
        #: The structure can be "singleton" or "trio" at the moment.
        structure = "singleton"
        #: The supported inheritance patterns are "denovo", "dominant", and "recessive" at the
        #: moment.  This is only used for non-singletons.  When dominant, the father will be
        #: affected.
        inheritance = "denovo"

    name = factory.LazyAttributeSequence(lambda o, n: "case %03d: %s" % (n, o.structure))
    index = factory.Sequence(lambda n: "index_%03d-N1-DNA1-WES1" % n)
    pedigree = []
    project = factory.SubFactory(ProjectFactory)

    @factory.lazy_attribute_sequence
    def pedigree(self, n):
        if self.structure not in ("singleton", "trio"):
            raise ValueError("Invalid structure type!")
        elif self.structure == "singleton":
            return [
                {
                    "patient": self.index,
                    "father": "0",
                    "mother": "0",
                    "sex": self.sex,
                    "affected": 2,
                    "has_gt_entries": True,
                }
            ]
        else:  # self.structure == "trio"
            # Father and mother name
            father = "father_%03d-N1-DNA1-WES1" % n
            mother = "mother_%03d-N1-DNA1-WES1" % n
            return [
                {
                    "patient": self.index,
                    "father": father,
                    "mother": mother,
                    "sex": self.sex,
                    "affected": 2,  # always affected
                    "has_gt_entries": True,
                },
                {
                    "patient": father,
                    "father": "0",
                    "mother": "0",
                    "sex": 1,  # always male
                    "affected": 2 if self.inheritance == "dominant" else 1,
                    "has_gt_entries": True,
                },
                {
                    "patient": mother,
                    "father": "0",
                    "mother": "0",
                    "sex": 2,  # always female
                    "affected": 1,  # never affected
                    "has_gt_entries": True,
                },
            ]


class SmallVariantQueryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SmallVariantQuery

    case = factory.SubFactory(CaseFactory)
    form_id = factory.Sequence(lambda n: str(n))
    form_version = factory.Sequence(lambda n: n)
    query_settings = factory.LazyAttribute(
        lambda o: vars(ResubmitFormDataFactory(names=o.case.get_members()))
    )
    name = factory.Sequence(lambda n: "SmallVariantQuery%d" % n)
    public = False


class ClinvarQueryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ClinvarQuery

    case = factory.SubFactory(CaseFactory)
    form_id = factory.Sequence(lambda n: str(n))
    form_version = factory.Sequence(lambda n: n)
    query_settings = factory.LazyAttribute(
        lambda o: vars(ResubmitClinvarFormDataFactory(names=o.case.get_members()))
    )
    name = factory.Sequence(lambda n: "ClinvarQuery%d" % n)
    public = False


class ProjectCasesSmallVariantQueryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProjectCasesSmallVariantQuery

    project = factory.SubFactory(ProjectFactory)
    form_id = factory.Sequence(lambda n: str(n))
    form_version = factory.Sequence(lambda n: n)
    query_settings = factory.LazyAttribute(
        lambda o: vars(ResubmitFormDataFactory(names=o.project.get_members()))
    )
    name = factory.Sequence(lambda n: "ProjectCasesSmallVariantQuery%d" % n)
    public = False


def default_genotypes():
    """Build default genotype pattern (het. in first, wild-type otherwise)."""
    yield {"gt": "0/1", "ad": 15, "dp": 30, "gq": 99}
    while True:
        yield {"gt": "0/0", "ad": 0, "dp": 30, "gq": 99}


def count_gt(*gts):
    """Return counter for the given genotypes."""

    def result(o):
        return len([x["gt"] for x in o.genotype.values() if x["gt"] in gts])

    return result


class SmallVariantFactory(factory.django.DjangoModelFactory):
    """Factory for creating ``SmallVariant`` objects.

    Allows creation of a finite set of actual variants from ``LAMA1`` gene.
    """

    class Meta:
        model = SmallVariant
        exclude = ["case"]

    class Params:
        #: The genotypes to create, by default only first is het. the rest is wild-type.
        genotypes = default_genotypes

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override to get rid of the ``case`` keyword argument and instead define ``case_id``."""
        manager = cls._get_manager(model_class)
        for db in ("refseq", "ensembl"):
            # Create the associated annotation entry
            AnnotationFactory(
                release=kwargs["release"],
                chromosome=kwargs["chromosome"],
                position=kwargs["position"],
                reference=kwargs["reference"],
                alternative=kwargs["alternative"],
                database=db,
                gene_id=kwargs["%s_gene_id" % db],
                transcript_id=kwargs["%s_transcript_id" % db],
            )
            # Create another entry for this variant, but different transcript
            AnnotationFactory(
                release=kwargs["release"],
                chromosome=kwargs["chromosome"],
                position=kwargs["position"],
                reference=kwargs["reference"],
                alternative=kwargs["alternative"],
                database=db,
                gene_id=kwargs["%s_gene_id" % db],
            )
        return manager.create(*args, **kwargs)

    release = "GRCh37"
    chromosome = factory.Iterator(list(map(str, range(1, 23))) + ["X", "Y"])
    position = factory.Sequence(lambda n: (n + 1) * 100)
    reference = factory.Iterator("ACGT")
    alternative = factory.Iterator("CGTA")
    var_type = "snv"
    #: Model pseudo-attribute, not stored in database.  Instead, ``case_id`` is stored.
    case = factory.SubFactory(CaseFactory)
    #: The actual reference to the case.
    case_id = factory.LazyAttribute(lambda o: o.case.id)

    @factory.lazy_attribute
    def genotype(self):
        """Generate genotype JSON field from already set ``self.case``."""
        return {line["patient"]: gt for line, gt in zip(self.case.pedigree, self.genotypes())}

    num_hom_alt = factory.LazyAttribute(count_gt("0/0"))
    num_hom_ref = factory.LazyAttribute(count_gt("1/1"))
    num_het = factory.LazyAttribute(count_gt("0/1", "1/0", "0|1", "1|0"))
    num_hemi_alt = 0
    num_hemi_ref = 0
    in_clinvar = False
    exac_frequency = 0.0001
    exac_homozygous = 0
    exac_heterozygous = 0
    exac_hemizygous = 0
    thousand_genomes_frequency = 0.0001
    thousand_genomes_homozygous = 0
    thousand_genomes_heterozygous = 0
    thousand_genomes_hemizygous = 0
    gnomad_exomes_frequency = 0.0001
    gnomad_exomes_homozygous = 0
    gnomad_exomes_heterozygous = 0
    gnomad_exomes_hemizygous = 0
    gnomad_genomes_frequency = 0.0001
    gnomad_genomes_homozygous = 0
    gnomad_genomes_heterozygous = 0
    gnomad_genomes_hemizygous = 0
    refseq_gene_id = factory.Sequence(lambda n: str(n))
    refseq_transcript_id = factory.Sequence(lambda n: "NM_%d" % n)
    refseq_transcript_coding = True
    refseq_hgvs_c = "c.123C>T"
    refseq_hgvs_p = "p.I2T"
    refseq_effect = factory.List(["synonymous_variant"])
    ensembl_gene_id = factory.Sequence(lambda n: "ENSG%d" % n)
    ensembl_transcript_id = factory.Sequence(lambda n: "ENST%d" % n)
    ensembl_transcript_coding = True
    ensembl_hgvs_c = "c.123C>T"
    ensembl_hgvs_p = "p.I2T"
    ensembl_effect = factory.List(["synonymous_variant"])


class SmallVariantSummaryFactory(factory.django.DjangoModelFactory):
    """Factory for ``SmallVariantSummary`` model."""

    class Meta:
        model = SmallVariantSummary

    release = "GRCh37"
    chromosome = factory.Iterator(list(map(str, range(1, 23))) + ["X", "Y"])
    position = factory.Sequence(lambda n: (n + 1) * 100)
    reference = factory.Iterator("ACGT")
    alternative = factory.Iterator("CGTA")
    count_hom_ref = 0
    count_het = 0
    count_hom_alt = 0
    count_hemi_ref = 0
    count_hemi_alt = 0


class FilterBgJobFactory(factory.django.DjangoModelFactory):
    """Factory for ``FilterBgJob`` model."""

    class Meta:
        model = FilterBgJob
        exclude = ["user"]

    # Dummy argument ``user`` to pass to subfactory BackgroundJobFactory
    user = None
    case = factory.SubFactory(CaseFactory)
    project = factory.LazyAttribute(lambda o: o.case.project)
    bg_job = factory.SubFactory(
        BackgroundJobFactory,
        project=factory.SelfAttribute("factory_parent.project"),
        user=factory.SelfAttribute("factory_parent.user"),
    )
    smallvariantquery = factory.SubFactory(
        SmallVariantQueryFactory,
        case=factory.SelfAttribute("factory_parent.case"),
        user=factory.SelfAttribute("factory_parent.user"),
    )


class ClinvarBgJobFactory(factory.django.DjangoModelFactory):
    """Factory for ``ClinvarBgJob`` model."""

    class Meta:
        model = ClinvarBgJob
        exclude = ["user"]

    # Dummy argument ``user`` to pass to subfactory BackgroundJobFactory
    user = None
    case = factory.SubFactory(CaseFactory)
    project = factory.LazyAttribute(lambda o: o.case.project)
    bg_job = factory.SubFactory(
        BackgroundJobFactory,
        project=factory.SelfAttribute("factory_parent.project"),
        user=factory.SelfAttribute("factory_parent.user"),
    )
    clinvarquery = factory.SubFactory(
        ClinvarQueryFactory,
        case=factory.SelfAttribute("factory_parent.case"),
        user=factory.SelfAttribute("factory_parent.user"),
    )


class ProjectCasesFilterBgJobFactory(factory.django.DjangoModelFactory):
    """Factory for ``ProjectCasesFilterBgJob`` model."""

    class Meta:
        model = ProjectCasesFilterBgJob
        exclude = ["user"]

    # Dummy argument ``user`` to pass to subfactory BackgroundJobFactory
    user = None
    project = factory.SubFactory(ProjectFactory)
    bg_job = factory.SubFactory(
        BackgroundJobFactory,
        project=factory.SelfAttribute("factory_parent.project"),
        user=factory.SelfAttribute("factory_parent.user"),
    )
    projectcasessmallvariantquery = factory.SubFactory(
        ProjectCasesSmallVariantQueryFactory,
        project=factory.SelfAttribute("factory_parent.project"),
        user=factory.SelfAttribute("factory_parent.user"),
    )


class DistillerSubmissionBgJobFactory(factory.django.DjangoModelFactory):
    """Factory for ``DistillerSubmissionBgJob`` model."""

    class Meta:
        model = DistillerSubmissionBgJob
        exclude = ["user"]

    # Dummy argument ``user`` to pass to subfactory BackgroundJobFactory
    user = None
    case = factory.SubFactory(CaseFactory)
    project = factory.LazyAttribute(lambda o: o.case.project)
    bg_job = factory.SubFactory(
        BackgroundJobFactory,
        project=factory.SelfAttribute("factory_parent.project"),
        user=factory.SelfAttribute("factory_parent.user"),
    )
    query_args = factory.LazyAttribute(
        lambda o: vars(ResubmitFormDataFactory(names=o.case.get_members()))
    )


class ExportFileBgJobFactory(factory.django.DjangoModelFactory):
    """Factory for ``ExportFileBgJob`` model."""

    class Meta:
        model = ExportFileBgJob
        exclude = ["user"]

    # Dummy argument ``user`` to pass to subfactory BackgroundJobFactory
    user = None
    case = factory.SubFactory(CaseFactory)
    project = factory.LazyAttribute(lambda o: o.case.project)
    bg_job = factory.SubFactory(
        BackgroundJobFactory,
        project=factory.SelfAttribute("factory_parent.project"),
        user=factory.SelfAttribute("factory_parent.user"),
    )
    query_args = factory.LazyAttribute(
        lambda o: vars(ResubmitFormDataFactory(names=o.case.get_members()))
    )
    file_type = "tsv"


class ExportFileJobResultFactory(factory.django.DjangoModelFactory):
    """Factory for ``ExportFileJobResult`` model."""

    class Meta:
        model = ExportFileJobResult
        exclude = ["user"]

    # Dummy argument ``user`` to pass to subfactory BackgroundJobFactory
    user = None
    job = factory.SubFactory(
        ExportFileBgJobFactory, user=factory.SelfAttribute("factory_parent.user")
    )
    payload = b"Testcontent"
    expiry_time = timezone.now()


class ExportProjectCasesFileBgJobFactory(factory.django.DjangoModelFactory):
    """Factory for ``ExportProjectCasesFileBgJobFactory`` model."""

    class Meta:
        model = ExportProjectCasesFileBgJob
        exclude = ["user"]

    # Dummy argument ``user`` to pass to subfactory BackgroundJobFactory
    user = None
    project = factory.SubFactory(ProjectFactory)
    bg_job = factory.SubFactory(
        BackgroundJobFactory,
        project=factory.SelfAttribute("factory_parent.project"),
        user=factory.SelfAttribute("factory_parent.user"),
    )
    query_args = factory.LazyAttribute(
        lambda o: vars(ResubmitFormDataFactory(names=o.project.get_members()))
    )
    file_type = "tsv"


class ExportProjectCasesFileBgJobResultFactory(factory.django.DjangoModelFactory):
    """Factory for ``ExportProjectCasesFileJobResult`` model."""

    class Meta:
        model = ExportProjectCasesFileBgJobResult
        exclude = ["user"]

    # Dummy argument ``user`` to pass to subfactory BackgroundJobFactory
    user = None
    job = factory.SubFactory(
        ExportProjectCasesFileBgJobFactory, user=factory.SelfAttribute("factory_parent.user")
    )
    payload = b"Testcontent"
    expiry_time = timezone.now()


class SmallVariantFlagsFactory(factory.django.DjangoModelFactory):
    """Factory for ``SmallVariantFlagsFactory`` model."""

    class Meta:
        model = SmallVariantFlags

    release = "GRCh37"
    chromosome = factory.Iterator(list(map(str, range(1, 23))) + ["X", "Y"])
    position = factory.Sequence(lambda n: (n + 1) * 100)
    reference = factory.Iterator("ACGT")
    alternative = factory.Iterator("CGTA")
    case = factory.SubFactory(CaseFactory)
    flag_bookmarked = True
    flag_candidate = False
    flag_final_causative = False
    flag_for_validation = False
    flag_visual = ""
    flag_validation = ""
    flag_phenotype_match = ""
    flag_summary = ""


class SmallVariantCommentFactory(factory.django.DjangoModelFactory):
    """Factory for ``SmallVariantComment`` model."""

    class Meta:
        model = SmallVariantComment

    release = "GRCh37"
    chromosome = factory.Iterator(list(map(str, range(1, 23))) + ["X", "Y"])
    position = factory.Sequence(lambda n: (n + 1) * 100)
    reference = factory.Iterator("ACGT")
    alternative = factory.Iterator("CGTA")
    user = None
    text = factory.Sequence(lambda n: "Comment %d" % n)
    case = factory.SubFactory(CaseFactory)