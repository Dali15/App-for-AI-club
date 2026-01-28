from django import forms
from .models import Project, ProjectFile, ProjectUpdate


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'category', 'repository_url', 'documentation_url', 'status', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Project name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Project description'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'repository_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'GitHub link'}),
            'documentation_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Docs link'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ProjectFileForm(forms.ModelForm):
    class Meta:
        model = ProjectFile
        fields = ['title', 'file_type', 'language', 'code_content', 'file', 'external_url', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'File name'}),
            'file_type': forms.Select(attrs={'class': 'form-select'}),
            'language': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Python, JavaScript'}),
            'code_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Paste code here...'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'external_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'External resource link'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
        }


class ProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = ProjectUpdate
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Update title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'What\'s new?'}),
        }
