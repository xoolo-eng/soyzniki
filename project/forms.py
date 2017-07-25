from django import forms
from re import compile, match
from project.models import Feedback


PHONE = compile('^(\s*)?(\+)?([- _():=+]?\d[- >():=+]?){10,14}(\s*)?$')
EMAIL = compile('^([\w]+)((.?|-?|_?)[\w]+)?@([\w-]{2,15}\.)+([\w]{2,6})$')


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(),
            'contact': forms.TextInput(),
        }

    def clean(self):
        if len(self.cleaned_data.get('name')) > 100:
            self.add_error('name', 'Не более 100 символов')
            raise forms.ValidationError('Ошибка ввода')
        if len(self.cleaned_data.get('contact')) > 100:
            self.add_error('contact', 'Не более 100 символов')
            raise forms.ValidationError('Ошибка ввода')
        elif not match(PHONE, self.cleaned_data.get('contact')):
            if not match(EMAIL, self.cleaned_data.get('contact')):
                self.add_error('contact', 'Номер телефона или email')
                raise forms.ValidationError('Ошибка ввода')
        if len(self.cleaned_data.get('message')) > 1000:
            self.add_error('message', 'Не более 1000 символов')
        return self.cleaned_data
