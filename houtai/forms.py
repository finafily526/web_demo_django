from django import forms
from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateTimeInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateTimeInput(attrs={'type': 'date'}))

class DateRangeForm1(forms.Form):
    start_date = forms.DateField(widget=forms.DateTimeInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateTimeInput(attrs={'type': 'date'}))
    list = ((1, u'一月'), (2, u'二月'), (3, u'三月'), (4, u'四月'), (5, u'五月'), (6, u'六月'),
            (7, u'七月'), (8, u'八月'), (9, u'九月'), (10, u'十月'), (11, u'十一月'), (12, u'十二月'),)
    obj_month = forms.CharField(widget=forms.widgets.Select(choices=list, attrs={'class': 'form-control'}), )
