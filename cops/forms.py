from django import forms
from cops.models import Cop, CaseCop

class FooForm(forms.Form):
    foo = forms.CharField(label='Your foo', max_length=100)


class CopForm(forms.Form):
    cop_choices = forms.ChoiceField(widget=forms.RadioSelect(),choices=(),required=False)
    note        = forms.CharField(widget=forms.Textarea,required=False)
    flag        = forms.BooleanField(required=False)
    def __init__(self,*args,**kwargs):
        choices   = kwargs.pop('choices')
        selection = kwargs.pop('selection')
        note      = kwargs.pop('note')
        flagged   = kwargs.pop('flagged')
        if choices is not None:
            try:
                super(CopForm,self).__init__(*args,**kwargs) # i don't understand this 
                self.fields['cop_choices'].choices = choices
                self.fields['cop_choices'].initial = selection
                self.fields['cop_choices'].label   = 'Which of these police officers is it?'
                self.fields['note'].initial        = note
                self.fields['note'].label          = 'Note'
                self.fields['flag'].label          = 'Flag for follow-up?'
                self.fields['flag'].initial        = flagged

            except Exception, e:
                import ipdb; ipdb.set_trace()
