from django import forms 
from .models import Account,UserProfile

class RegistratioForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        
        'placeholder':'Enter Password',
        'class':'form-control',
        
        }))
    
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
        
        'placeholder':'Confirm Password'
    }))
    class Meta:
        model=Account
        fields=['first_name','last_name','email','phone_number','password']  
        
    def __init__(self,*args, **kwargs):
        super(RegistratioForm,self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder']='Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder']='Enter last Name'
        self.fields['phone_number'].widget.attrs['placeholder']='Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder']='Enter Email Adreess'

        
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
            
            
    def clean(self):
        clean_data=super(RegistratioForm,self).clean()
        password=clean_data.get('password')
        confirm_password=clean_data.get('confirm_password')
        
        
        if password !=confirm_password:
            raise forms.ValidationError(
                "password doesnot match"
            )            
class UserForm(forms.ModelForm):
    class Meta:
        model=Account
        fields=('first_name','last_name','phone_number')
        
    def __init__(self,*args, **kwargs):
        super(UserForm,self).__init__(*args, **kwargs) 
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'   
        
        
class UserProfileForm(forms.ModelForm):
    #profile_picture=forms.ImageField(required=False,error_messages={'invalid':('image files only')},widget=forms.FileInput)
    class Meta:
        model=UserProfile
        fields=('address_line_1','address_line_2','city','state','country')
        
    def __init__(self,*args, **kwargs):
        super(UserProfileForm,self).__init__(*args, **kwargs) 
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'          