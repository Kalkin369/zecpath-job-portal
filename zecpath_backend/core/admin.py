from django.contrib import admin
from core.models import (User, Job, Application, Employer, Candidate, ApplicationLog,NotificationLog,AIInterviewSession,AIQuestion,
                     AIAnswer,AICall,CallLog,InterviewState,QuestionTemplate,SavedJob,AnswerEvaluation,InterviewSchedule,AvailabilitySlot)


#  User Admin
class UserAdmin(admin.ModelAdmin):
    list_display = ('id',  'email', 'role', 'created_at','is_active','is_verified')
    search_fields = ( 'email',)
    list_filter = ('role',)
    ordering = ('-created_at',)


#  Employer Admin
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'user', 'is_verified')
    search_fields = ('company_name', 'user__email')
    list_filter = ('is_verified',)
    ordering = ('id',)


#  Candidate Admin
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'qualification', 'experience')
    search_fields = ('user__email', 'phone')
    ordering = ('id',)

class ApplicationInline(admin.TabularInline):
    model = Application
    extra = 0


#  Job Admin
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'employer', 'experience','status', 'created_at')
    search_fields = ('title', 'skills')
    list_filter = ('status','job_type')
    ordering = ('-created_at',)
    inlines = [ApplicationInline]

#  Application Admin
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'candidate', 'job', 'status', 'ats_score', 'applied_at')
    search_fields = ('candidate__user__email', 'job__title')
    list_filter = ('status',)
    ordering = ('-applied_at',)

class ApplicationLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'application', 'old_status', 'new_status', 'changed_at')
    search_fields = ('application__candidate__user__email',)
    list_filter = ('new_status',)
    ordering = ('-changed_at',)

class NotificationLogAdmin(admin.ModelAdmin):

    list_display = ('id','user','subject','status','created_at')

    search_fields = ('user__email','subject')

    list_filter = ('status',)

    readonly_fields = ('created_at',)

    ordering = ('-created_at',)  

class SavedJobAdmin(admin.ModelAdmin):

    list_display = ('id','candidate','job','saved_at')

    search_fields = ('candidate__user__email','job__title')

    ordering = ('-saved_at',)      

class AICallAdmin(admin.ModelAdmin):

    list_display = ('id','application','status','retry_count','created_at')

    search_fields = ('application__candidate__user__email',)

    list_filter = ('status',)

    ordering = ('-created_at',)  

class AIInterviewSessionAdmin(admin.ModelAdmin):

    list_display = ('id','ai_call','status','started_at')

    search_fields = ('ai_call__id',)

    list_filter = ('status',)

    ordering = ('-started_at',)


class AIQuestionAdmin(admin.ModelAdmin):

    list_display = ('id','session','template','created_at')

    search_fields = ('question_text',)

    ordering = ('-created_at',)



class AIAnswerAdmin(admin.ModelAdmin):

    list_display = ('id','question','score','created_at')

    search_fields = ('answer_text',)

    ordering = ('-created_at',) 

class CallLogAdmin(admin.ModelAdmin):

    list_display = ('id','ai_call','event','triggered_by','created_at')

    search_fields = ('event','triggered_by')

    ordering = ('-created_at',)




class InterviewStateAdmin(admin.ModelAdmin):

    list_display = ('id','session','current_question_index','current_category','is_completed')

    list_filter = ('is_completed','current_category') 

class QuestionTemplateAdmin(admin.ModelAdmin):

    list_display = ('id','role','category','is_follow_up','created_at')

    search_fields = ('role','question')

    list_filter = ('role','category','is_follow_up')

    ordering = ('role','category') 



class AnswerEvaluationAdmin(admin.ModelAdmin):

    list_display = ('id','answer','total_score','created_at')

    ordering = ('-created_at',) 

class InterviewScheduleAdmin(admin.ModelAdmin):

    list_display = ('id','application','scheduled_at','status','created_at')

    list_filter = ('status',)

    ordering = ('-scheduled_at',)


class AvailabilitySlotAdmin(admin.ModelAdmin):

    list_display = ('id','role','start_time','end_time','is_booked')

    list_filter = ('is_booked','role')

    ordering = ('start_time',)    



#  Register
admin.site.register(User, UserAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Employer, EmployerAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(ApplicationLog, ApplicationLogAdmin)
admin.site.register(NotificationLog,NotificationLogAdmin)
admin.site.register(SavedJob,SavedJobAdmin)
admin.site.register(AICall,AICallAdmin)
admin.site.register(AIInterviewSession,AIInterviewSessionAdmin)
admin.site.register(AIQuestion,AIQuestionAdmin)
admin.site.register(AIAnswer,AIAnswerAdmin)
admin.site.register(CallLog,CallLogAdmin)
admin.site.register(InterviewState,InterviewStateAdmin)
admin.site.register(QuestionTemplate,QuestionTemplateAdmin)
admin.site.register(AnswerEvaluation,AnswerEvaluationAdmin)
admin.site.register(InterviewSchedule,InterviewScheduleAdmin)
admin.site.register(AvailabilitySlot,AvailabilitySlotAdmin)