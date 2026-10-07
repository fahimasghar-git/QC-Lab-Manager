from django.contrib import admin
from unfold.admin import ModelAdmin
from .pdf_utils import generate_iso_pdf
from .models import (
    PersonnelAuthorizationPermit,
    AnalystAuthorizationTestInstrument,
    AnalystAuthorizationProduct,
    CompetencyEvalInternalSample,
    CompetencyEvalPTSample,
    GradingMatrixEquipment,
    GradingMatrixProduct,
    GradingMatrixDocument,
    AuthorizedAnalystList,
    TechnicalPersonnelList
)

class AnalystAuthorizationTestInstrumentInline(admin.TabularInline):
    model = AnalystAuthorizationTestInstrument
    extra = 1

class AnalystAuthorizationProductInline(admin.TabularInline):
    model = AnalystAuthorizationProduct
    extra = 1

@admin.register(PersonnelAuthorizationPermit)
class PersonnelAuthorizationPermitAdmin(ModelAdmin):
    actions = [generate_iso_pdf]
    list_display = ['analyst', 'issue_date', 'valid_until', 'authorized_by']
    inlines = [AnalystAuthorizationTestInstrumentInline, AnalystAuthorizationProductInline]

@admin.register(CompetencyEvalInternalSample)
class CompetencyEvalInternalSampleAdmin(ModelAdmin):
    actions = [generate_iso_pdf]
    list_display = ['analyst', 'evaluation_date', 'parameter_tested', 'result_status']

@admin.register(CompetencyEvalPTSample)
class CompetencyEvalPTSampleAdmin(ModelAdmin):
    actions = [generate_iso_pdf]
    list_display = ['analyst', 'evaluation_date', 'parameter_tested', 'z_score', 'result_status']

@admin.register(GradingMatrixEquipment)
class GradingMatrixEquipmentAdmin(ModelAdmin):
    actions = [generate_iso_pdf]
    list_display = ['analyst', 'equipment_name', 'date', 'overall_grade']

@admin.register(GradingMatrixProduct)
class GradingMatrixProductAdmin(ModelAdmin):
    actions = [generate_iso_pdf]
    list_display = ['analyst', 'product_category', 'date', 'overall_grade']

@admin.register(GradingMatrixDocument)
class GradingMatrixDocumentAdmin(ModelAdmin):
    actions = [generate_iso_pdf]
    list_display = ['analyst', 'date', 'overall_grade']

@admin.register(AuthorizedAnalystList)
class AuthorizedAnalystListAdmin(ModelAdmin):
    actions = [generate_iso_pdf]
    list_display = ['revision_number', 'date_issued', 'approved_by']

@admin.register(TechnicalPersonnelList)
class TechnicalPersonnelListAdmin(ModelAdmin):
    actions = [generate_iso_pdf]
    list_display = ['revision_number', 'date_issued', 'approved_by']
