import json
from django import forms
from django.forms import formsets
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
#from django.views.generic.simple import direct_to_template
from django.shortcuts import render


from ajax_form.form_serializer import FormSerializer
from ajax_form.utils import json_response


class ExampleForm(forms.Form):
    name = forms.CharField(label='user name',
            help_text="is name", min_length=2, max_length=20)
    is_active = forms.BooleanField(initial=True)
    gender = forms.ChoiceField(choices=[('m', 'male'), ('f', 'female')])
    love_eat = forms.MultipleChoiceField(
            choices=[('meat', 'meat'), ('beer', 'beer'), ('cheese', 'cheese')])

    is_marred = forms.ChoiceField(
            choices=[('y', 'yes'), ('no', 'no')],
            widget=forms.RadioSelect(attrs={'class': 'nya'})
            )
    
    #If you want add errors ( To Example Form), uncomment this.
'''
    def clean(self):
        if not self.errors:
            raise forms.ValidationError(u"Example error in clean")
        return self.cleaned_data
'''
def index(request):
    if request.POST:
        form = ExampleForm(data=request.POST)
    else:
        form = ExampleForm()

    if request.is_ajax():
        form_dict = FormSerializer().serialize(form)
        return json_response(form_dict, request)

    return render(request, 'ajax_form.html', {'form': form})

def ajax_formset(request):
    formset_class = formsets.formset_factory(ExampleForm)
    rdict = {'validForm':'true'}
    if request.POST:
        formset = formset_class(data=request.POST)
        if formset.is_valid():
            rdict.update({'validForm':'false'})        
    else:
        formset = formset_class()        

    if request.is_ajax():                
        formset_dict = FormSerializer().serialize(formset)              
        rdict.update({'form': formset_dict  })
        return json_response(rdict, request)

    return render(request, 'ajax_formset.html', {'formset': rdict})
    
