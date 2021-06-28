from django.forms import widgets, ModelForm, ValidationError
from .models import UserProfile
from django.core.files.images import get_image_dimensions


class UserProfileForm(ModelForm):
    class Meta:
        model= UserProfile
        fields= [
            'email',
            'f_name', 'l_name', 
            'bio', 'b_date',
            'pfp', 'pgp','gender'
        ]
        GENDER_CHOICES = {
            ('M', 'Male'),
            ('F', 'Female'),
        }
        exclude={'user', 'fullName'}
        widgets = {
            'email': widgets.EmailInput(),
            'b_date': widgets.SelectDateWidget(),
            'gender': widgets.RadioSelect(choices=GENDER_CHOICES),
            'f_name': widgets.TextInput(),
            'l_name': widgets.TextInput(),
            'bio': widgets.TextInput(),
            'user': widgets.TextInput(),
            'fullName': widgets.TextInput(),
        }
    def clean_pgp(self):
        pgp= self.cleaned_data.get('pgp')
        if not pgp:
            raise ValidationError("no background image !")
        else:
            w,h= get_image_dimensions(pgp)
            if w <  2037 :
                raise ValidationError('the image width is %i , its suppose to be 820'%w)
            if h <  754 :
                raise ValidationError('the image width is %i , its suppose to be 312'%h)
            return pgp