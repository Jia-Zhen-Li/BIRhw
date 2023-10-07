from django import forms

class Query(forms.Form): 
    query = forms.CharField(max_length=50,
                          widget=forms.TextInput(attrs={'placeholder': 'Insert the query'}))
