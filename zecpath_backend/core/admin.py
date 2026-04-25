from django.contrib import admin
from .models import User, Job, Application, Employer, Candidate


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
    list_display = ('id', 'candidate', 'job', 'status', 'ats_score', 'created_at')
    search_fields = ('candidate__user__email', 'job__title')
    list_filter = ('status',)
    ordering = ('-created_at',)


#  Register
admin.site.register(User, UserAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Employer, EmployerAdmin)
admin.site.register(Candidate, CandidateAdmin)