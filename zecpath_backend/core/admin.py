from django.contrib import admin
from .models import User, Job, Application, Employer, Candidate


#  User Admin
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'role', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('role',)
    ordering = ('-created_at',)


#  Employer Admin
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'user', 'is_verified')
    search_fields = ('company_name', 'user__name')
    list_filter = ('is_verified',)
    ordering = ('id',)


#  Candidate Admin
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'qualification', 'experience')
    search_fields = ('user__name', 'phone')
    ordering = ('id',)

class ApplicationInline(admin.TabularInline):
    model = Application
    extra = 0


#  Job Admin
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'employer', 'experience_required', 'created_at')
    search_fields = ('title', 'required_skills')
    list_filter = ('experience_required',)
    ordering = ('-created_at',)
    inlines = [ApplicationInline]

#  Application Admin
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'candidate', 'job', 'status', 'ats_score', 'created_at')
    search_fields = ('candidate__user__name', 'job__title')
    list_filter = ('status',)
    ordering = ('-created_at',)


#  Register
admin.site.register(User, UserAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Employer, EmployerAdmin)
admin.site.register(Candidate, CandidateAdmin)