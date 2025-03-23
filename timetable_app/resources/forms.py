from django import forms
from .models import Room ,Domain ,Formation ,Module ,Teacher ,Group ,Course
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import timedelta

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'capacity']
        
class DomainForm(forms.ModelForm):
    class Meta:
        model = Domain
        fields = ['name']

class FormationForm(forms.ModelForm):
    class Meta:
        model = Formation
        fields = ['name', 'domain']

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['name', 'code', 'formation', 'total_duration', 'session_duration']

class TeacherForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Teacher
        fields = ['name']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ce nom d'utilisateur existe déjà.")
        return username
    
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'formation', 'student_count']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['module', 'teacher', 'room', 'group', 'start_time', 'end_time', 'day_of_week', 'start_date', 'total_sessions', 'card_color']

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        start_date = cleaned_data.get('start_date')
        day_of_week = cleaned_data.get('day_of_week')

        # Vérifier que l'heure de début est avant l'heure de fin
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("L'heure de début doit être antérieure à l'heure de fin.")

        # Vérifier que la date de début correspond au jour de la semaine sélectionné
        if start_date and day_of_week:
            if start_date.strftime('%A') != day_of_week:
                raise forms.ValidationError(f"La date de début doit correspondre au jour sélectionné ({day_of_week}).")

        return cleaned_data