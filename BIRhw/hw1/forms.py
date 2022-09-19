from django import forms

class UploadFileForm(forms.Form): # 上傳檔案
    file = forms.FileField() #label='Upload File'
    keyword = forms.CharField(max_length=50,
                          widget=forms.TextInput(attrs={'placeholder': 'Insert the keyword'})) 

class Get_Url(forms.Form):
    url = forms.CharField(max_length=100,
                          widget=forms.TextInput(attrs={'placeholder': 'Insert the url'})) #url to parser
    keyword = forms.CharField(max_length=50,
                          widget=forms.TextInput(attrs={'placeholder': 'Insert the keyword'})) 