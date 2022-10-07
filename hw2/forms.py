from django import forms

class UploadFileForm_zipf(forms.Form): 
    file = forms.FileField() 
    keyword = forms.CharField(max_length=50,
                          widget=forms.TextInput(attrs={'placeholder': 'Insert the keyword'}))
    ranks = forms.IntegerField(
                          widget=forms.TextInput(attrs={'placeholder': 'Insert the number of output ranks'})) 

class Get_Url_zipf(forms.Form):
    web_list = ['PUBMED','TWITTER']
    webtype = forms.ChoiceField(choices=web_list)
    term = forms.CharField(max_length=100,
                          widget=forms.TextInput(attrs={'placeholder': 'Insert the url'}))  # search to scrape
    size = forms.IntegerField(                                                              # how much data to search 
                          widget=forms.TextInput(attrs={'placeholder': 'Insert the number of output ranks'})) 
    keyword = forms.CharField(max_length=50,                                                # search in texts
                          widget=forms.TextInput(attrs={'placeholder': 'Insert the keyword'})) 
    ranks = forms.IntegerField(
                          widget=forms.TextInput(attrs={'placeholder': 'Insert the number of output ranks'})) 