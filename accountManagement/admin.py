from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms

from .models import User, Course, StudentClass, Module

from django.contrib.auth.models import Group

admin.site.unregister(Group)


# Register your models here.

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0
    max_num = 0
    readonly_fields = ('moduleName',)
    can_delete = False


class CourseAdmin(admin.ModelAdmin):

    readonly_fields = ('id', )

    fieldsets = (
        (None, {'fields': ('courseName',)}),
        ('Details', {'fields': ('courseInstitution',
         'courseDescription', 'quizTags', 'id')}),
    )
    inlines = [ModuleInline, ]

    def __str__(self):
        return self.courseName


class StudentAdminForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_('Users'),
            is_stacked=False
        )
    )

    class Meta:
        model = StudentClass
        exclude = tuple()

    def __init__(self, *args, **kwargs):
        super(StudentAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['users'].initial = self.instance.users.all()

    def save(self, commit=True):
        studentclass = super(StudentAdminForm, self).save(commit=False)

        if commit:
            studentclass.save()

        if studentclass.pk:
            studentclass.users.set(self.cleaned_data['users'])
            self.save_m2m()

        return studentclass


"""
class StudentAdminForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_('Users'),
            is_stacked=False
        )
    )

    class Meta:
        model = StudentClass
        exclude = tuple()

    def __init__(self, *args, **kwargs):
        super(StudentAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk and hasattr(self.instance, 'className'):
            print(vars(self.instance))
            self.fields['users'].initial = User.objects.filter(
                classes__id=self.instance.id)

    def save(self, commit=True):
        studentclass = super(StudentAdminForm, self).save(commit=False)

        if commit:
            studentclass.save()

        if studentclass.pk:
            studentclass.users = self.cleaned_data['users']
            self.save_m2m()

        return studentclass
"""


class StudentClassAdmin(admin.ModelAdmin):

    form = StudentAdminForm

    filter_horizontal = ('courses',)

    def __str__(self):
        return self.className


class ModuleAdmin(admin.ModelAdmin):

    readonly_fields = ('id', )

    fieldsets = (
        (None, {'fields': ('moduleName',)}),
        ('Details', {'fields': ('course', 'id', )}),
    )

    def __str__(self):
        return self.moduleName


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = '__all__'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdmin(BaseUserAdmin):
    list_filter = ("accountType", )
    list_display = list(BaseUserAdmin.list_display)
    list_display.insert(-1, "designation")

    add_form = UserCreationForm

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': (
            'first_name', 'last_name', 'email', 'phoneNumber', 'profilePic', )}),
        ('Administration info', {'fields': (
            'startDate', 'designation', 'accountType', 'institution', 'notificationAccess')}),
        ('Course info', {'fields': ('classes', )}),
        # ('Quiz Responses', {'fields': ('quizResponses', )}),
        ('Time Online', {'fields': ('timeOnline', )}),
        ('Permissions', {'fields': ('is_staff', 'groups',)}),
        # ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'phoneNumber', 'first_name', 'last_name', 'accountType', 'institution', 'classes',)}
         ),
    )
    filter_horizontal = ('classes',)

    def __str__(self):
        return self.username


admin.site.register(User, UserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(StudentClass, StudentClassAdmin)
admin.site.register(Module, ModuleAdmin)
