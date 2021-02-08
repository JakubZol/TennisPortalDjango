from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from .models import Player
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Player
        fields = ('id', 'username', 'first_name', 'last_name', 'gender', 'weight', 'height', 'ntrp', 'plays', 'backhand', 'birthdate')

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


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Player
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'gender', 'weight', 'height', 'ntrp', 'plays', 'backhand', 'birthdate')

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('id', 'email', 'username', 'first_name', 'last_name', 'gender', 'weight', 'height', 'ntrp', 'plays', 'backhand', 'birthdate', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username', 'id')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'gender', 'weight', 'height', 'ntrp', 'plays', 'backhand', 'birthdate',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('password1', 'password2', 'email', 'username', 'gender', 'weight', 'height', 'first_name', 'last_name', 'ntrp', 'plays', 'backhand', 'birthdate', ),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(Player, UserAdmin)
admin.site.unregister(Group)
