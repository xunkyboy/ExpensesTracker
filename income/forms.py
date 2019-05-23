from django import forms
from .models import Income
import datetime

class IncomeForm(forms.ModelForm):
    title=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    description= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    date = forms.CharField(initial=datetime.date.today,widget=forms.DateInput(attrs={'class': 'form-control','type':'date'}))
    rupees = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    class Meta:
        model=Income
        fields=['title','description','date','rupees']