from django import forms
from comments.models import Comments


class CommentsForm(forms.ModelForm):
    '''
    Форма добавление комментария к записи
    '''
    class Meta:
        model = Comments
        fields = '__all__'
        exclude = ['title']
        widgets = {
            'applications': forms.HiddenInput(),
            'model': forms.HiddenInput(),
            'record_id': forms.HiddenInput(),
            'user': forms.HiddenInput()
        }
