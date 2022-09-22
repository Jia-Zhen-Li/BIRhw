from django import forms

class UploadFileForm_counter(forms.Form): # 上傳檔案
    file = forms.FileField() #label='Upload File'
    keyword = forms.CharField(max_length=50,
                          widget=forms.TextInput(attrs={'placeholder': 'Insert the keyword'})) 

class Get_Url_counter(forms.Form):
    url = forms.CharField(max_length=100,
                          widget=forms.TextInput(attrs={'placeholder': 'Insert the url'})) #url to parser
    keyword = forms.CharField(max_length=50,
                          widget=forms.TextInput(attrs={'placeholder': 'Insert the keyword'})) 

class UploadFileForm_zipf(forms.Form): # 上傳檔案
    file = forms.FileField() #label='Upload File'
    keyword = forms.CharField(max_length=50,
                          widget=forms.TextInput(attrs={'placeholder': 'Insert the keyword'}))
    ranks = forms.CharField(max_length=50,
                          widget=forms.TextInput(attrs={'placeholder': 'Insert the number of output ranks'})) 

class Get_Url_zipf(forms.Form):
    url = forms.CharField(max_length=100,
                          widget=forms.TextInput(attrs={'placeholder': 'Insert the url'})) #url to parser
    keyword = forms.CharField(max_length=50,
                          widget=forms.TextInput(attrs={'placeholder': 'Insert the keyword'})) 
    ranks = forms.CharField(max_length=50,
                          widget=forms.TextInput(attrs={'placeholder': 'Insert the number of output ranks'})) 