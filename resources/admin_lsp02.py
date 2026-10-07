from django.contrib import admin
from unfold.admin import ModelAdmin
from .pdf_utils import generate_iso_pdf
from .models import (
    TrainingNeedAssessment,
    AnnualTrainingPlan,
    TrainingPlanItem,
    TrainingAttendanceSheet,
    AttendanceRecord,
    TrainingEvaluation,
    TrainingFeedback,
    IndividualTrainingRecord,
    OrientationPlan,
    CompetenceReassessment,
    TrainerEvaluation
)

@admin.register(TrainingNeedAssessment)
class TrainingNeedAssessmentAdmin(ModelAdmin):
    actions = [generate_iso_pdf]
    list_display = ['analyst', 'assessment_year', 'total_percentage', 'approved_by']

class TrainingPlanItemInline(admin.TabularInline):
    model = TrainingPlanItem
    extra = 1

@admin.register(AnnualTrainingPlan)
class AnnualTrainingPlanAdmin(ModelAdmin):
    actions = [generate_iso_pdf]
    list_display = ['plan_no', 'month_year', 'prepared_by', 'approved_by']
    inlines = [TrainingPlanItemInline]

class AttendanceRecordInline(admin.TabularInline):
    model = AttendanceRecord
    extra = 1

@admin.register(TrainingAttendanceSheet)
class TrainingAttendanceSheetAdmin(ModelAdmin):
    actions = [generate_iso_pdf]
    list_display = ['reference', 'title', 'date_held', 'instructor']
    inlines = [AttendanceRecordInline]

@admin.register(TrainingEvaluation)
class TrainingEvaluationAdmin(ModelAdmin):
    actions = [generate_iso_pdf]
    list_display = ['analyst', 'training', 'evaluation_date', 'score']

@admin.register(TrainingFeedback)
class TrainingFeedbackAdmin(ModelAdmin):
    actions = [generate_iso_pdf]
    list_display = ['analyst', 'training', 'overall_rating']
    
    def overall_rating(self, obj):
        return f"{(obj.content_rating + obj.instructor_rating)/2}/5"

@admin.register(IndividualTrainingRecord)
class IndividualTrainingRecordAdmin(ModelAdmin):
    actions = [generate_iso_pdf]
    list_display = ['analyst', 'training_title', 'date_completed', 'verified_by']

@admin.register(OrientationPlan)
class OrientationPlanAdmin(ModelAdmin):
    actions = [generate_iso_pdf]
    list_display = ['analyst', 'department', 'start_date', 'mentor']

@admin.register(CompetenceReassessment)
class CompetenceReassessmentAdmin(ModelAdmin):
    actions = [generate_iso_pdf]
    list_display = ['analyst', 'date', 'outcome', 'evaluator']

@admin.register(TrainerEvaluation)
class TrainerEvaluationAdmin(ModelAdmin):
    actions = [generate_iso_pdf]
    list_display = ['trainer', 'date', 'overall_rating', 'evaluator']

