from django import forms
from re import compile, match
from user.models import User, Secret
from soyzniki.models import Country, Region, District, City
from soyzniki.main.auth import hash_user_pass


# Regular expressions for validation
PHONE = compile('^(\s*)?(\+)?([- _():=+]?\d[- >():=+]?){10,14}(\s*)?$')
EMAIL = compile('^[-\w.]+@([A-z0-9][-A-z0-9]+\.)?([A-z0-9][-A-z0-9]+\.)+[A-z]{2,6}$')
LOGIN = compile('^[a-zA-Z0-9_]{3,25}$')
NAME = compile('^[а-яА-ЯёЁa-zA-Z-]{2,50}$')
STREET = compile('^[а-яА-ЯёЁa-zA-Z0-9-_, \./]{3,150}$')
PASSWORD = compile('[A-zА-яЁё0-9*/<>_-]{8,50}')


list_closed_login = [
    'admin',
    'add',
    'login',
    'logout',
    'edit',
    'edit_pass',
    'delete',
    'activate',
    'root',
]


# Form for adding a user
class NewUser(forms.Form):
    login = forms.CharField(
        max_length=25,
        label='Имя пользователя/Login',
        widget=forms.TextInput(
            attrs={
                'id': 'login',
            }),
        error_messages={
            'required': 'Придумайте имя пользователя/Login'
        }
    )
    name = forms.CharField(
        max_length=50,
        label='Ваше имя',
        widget=forms.TextInput(
            attrs={
                'id': 'name',
            }),
        error_messages={
            'required': 'Введите Ваше имя'
        }
    )
    family = forms.CharField(
        max_length=50,
        label='Ваша фамилия',
        widget=forms.TextInput(
            attrs={
                'id': 'family',
            }),
        error_messages={
            'required': 'Введите Вашу фамилию'
        }
    )
    email = forms.CharField(
        max_length=50,
        label='Ваш email',
        widget=forms.EmailInput(
            attrs={
                'id': 'email',
            }),
        error_messages={
            'required': 'Введите Ваш email'
        }
    )
    telephone = forms.CharField(
        max_length=25,
        label='Ваш номер телефонa',
        widget=forms.TextInput(
            attrs={
                'id': 'telephone',
            }),
        error_messages={
            'required': 'Введите Ваш номер телефонa'
        }
    )
    country = forms.CharField(
        max_length=255,
        label='Страна',
        widget=forms.TextInput(
            attrs={
                'id': 'country',
                'class': 'custom_input',
            }),
        error_messages={
            'required': 'Введите Страну'
        }
    )
    region = forms.CharField(
        max_length=255,
        label='Регион / Область',
        widget=forms.TextInput(
            attrs={
                'id': 'region',
                'class': 'custom_input',
            }),
        error_messages={
            'required': 'Введите Регион / Область'
        }
    )
    district = forms.CharField(
        max_length=255,
        label='Район',
        widget=forms.TextInput(
            attrs={
                'id': 'district',
                'class': 'custom_input',
            }),
        error_messages={
            'required': 'Введите район'
        }
    )
    city = forms.CharField(
        max_length=255,
        label='Населенный пункт',
        widget=forms.TextInput(
            attrs={
                'id': 'city',
                'class': 'custom_input',
            }),
        error_messages={
            'required': 'Введите населенный пункт'
        }
    )
    street = forms.CharField(
        max_length=150,
        label='Улица, корпус, дом, квартира',
        widget=forms.TextInput(
            attrs={
                'id': 'street',
            }),
        error_messages={
            'required': 'Введите улицу, корпус, дом, квартиру'
        }
    )
    password = forms.CharField(
        max_length=50,
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={
                'id': 'password',
            }),
        error_messages={
            'required': 'Введите пароль'
        }
    )
    password_repeat = forms.CharField(
        max_length=50,
        label='Подтверждение пароля',
        widget=forms.PasswordInput(
            attrs={
                'id': 'password_repeat',
            }),
        error_messages={
            'required': 'Введите подтверждение пароля'
        }
    )
    agreement = forms.BooleanField(
        label='Согласен с <a href="/licens/agreement/">приавилами использования</a>',
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'id': 'agreement',
                'checked': 'checked',
            })
    )
    country_id = forms.IntegerField(
        widget=forms.HiddenInput(attrs={
            'id': 'country_id'
        })
    )
    region_id = forms.IntegerField(
        widget=forms.HiddenInput(attrs={
            'id': 'region_id'
        })
    )
    district_id = forms.IntegerField(
        widget=forms.HiddenInput(attrs={
            'id': 'district_id'
        })
    )
    city_id = forms.IntegerField(
        widget=forms.HiddenInput(attrs={
            'id': 'city_id'
        })
    )

    # Method for saving data Forms for adding a user to the user model
    def save(self):
        new_user = User(
            login=self.cleaned_data.get('login'),
            name=self.cleaned_data.get('name'),
            family=self.cleaned_data.get('family'),
            email=self.cleaned_data.get('email'),
            telephone=self.cleaned_data.get('telephone'),
            country_id=self.cleaned_data.get('country_id'),
            region_id=self.cleaned_data.get('region_id'),
            district_id=self.cleaned_data.get('district_id'),
            city_id=self.cleaned_data.get('city_id'),
            street=self.cleaned_data.get('street'),
            hash_passwd=self.cleaned_data.get('password')
        )
        new_user.save()

    # method for form validation data to add a user
    def clean(self):
        if self.cleaned_data.get('login') in list_closed_login:
            self.add_error('login', 'Данное имя пользователя закрыто для регистрации')
            raise forms.ValidationError('Ошибка ввода')
        try:
            user = User.objects.get(login=self.cleaned_data.get('login'))
        except User.DoesNotExist:
            if not match(LOGIN, self.cleaned_data.get('login')):
                self.add_error('login', 'Допускаются только латинские символы и _')
                raise forms.ValidationError('Ошибка ввода')
        else:
            self.add_error('login', 'Имя пользователя {} уже занято'.format(user.login))
            raise forms.ValidationError('Ошибка ввода')

        if not match(NAME, self.cleaned_data.get('name')):
            self.add_error('name', 'Допускаются только русские, латинские символы')
            raise forms.ValidationError('Ошибка ввода')

        if not match(NAME, self.cleaned_data.get('family')):
            self.add_error('family', 'Допускаются только русские, латинские символы')
            raise forms.ValidationError('Ошибка ввода')

        if not match(EMAIL, self.cleaned_data.get('email')):
            self.add_error('email', 'Email не соответствует шаблону')
            raise forms.ValidationError('Ошибка ввода')

        if not match(PHONE, self.cleaned_data.get('telephone')):
            self.add_error('telephone', 'Номер не соответствует шаблону')
            raise forms.ValidationError('Ошибка ввода')

        try:
            country = Country.objects.get(name_ru=self.cleaned_data.get('country'))
        except Country.DoesNotExist:
            self.add_error('country', 'Данной страны нет в базе данных')
            raise forms.ValidationError('Ошибка ввода')
        else:
            pass

        try:
            region = Region.objects.get(
                country_id=country.id,
                name_ru=self.cleaned_data.get('region')
            )
        except Region.DoesNotExist:
            self.add_error('region', 'Данного региона / области нет в базе данных')
            raise forms.ValidationError('Ошибка ввода')
        else:
            pass

        try:
            district = District.objects.get(
                region_id=region.id,
                name_ru=self.cleaned_data.get('district')
            )
        except District.DoesNotExist:
            self.add_error('district', 'Данного районного центра нет в базе данных')
            raise forms.ValidationError('Ошибка ввода')
        else:
            pass

        try:
            City.objects.get(
                district_id=district.id,
                name_ru=self.cleaned_data.get('city')
            )
        except City.DoesNotExist:
            self.add_error('city', 'Данного населенного пункта нет в базе данных')
            raise forms.ValidationError('Ошибка ввода')
        else:
            pass

        if not match(STREET, self.cleaned_data.get('street')):
            self.add_error('street', 'Используются не поддерживаемые символы')
            raise forms.ValidationError('Ошибка ввода')

        if not match(PASSWORD, self.cleaned_data.get('password')):
            self.add_error('password', 'Пароль от 8-и до 50-и символов')
            raise forms.ValidationError('Ошибка ввода ')

        if self.cleaned_data.get('password') != self.cleaned_data.get('password_repeat'):
            self.add_error('password_repeat', 'Пароли не совподают')
            raise forms.ValidationError('Ошибка ввода')
        if not self.cleaned_data.get('agreement'):
            self.add_error('agreement', 'Для регистрации необходимо принять условия использования')
            raise forms.ValidationError('Ошибка ввода')

        return self.cleaned_data


class LoginUser(forms.Form):
    user = forms.CharField(
        max_length=25,
        label='Имя пользователя/Login',
        widget=forms.TextInput(
            attrs={
                'id': 'user',
            }),
        error_messages={
            'required': 'Введите имя пользователя',
        }
    )
    password = forms.CharField(
        max_length=50,
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={
                'id': 'password',
            }),
        error_messages={
            'required': 'Ведите пароль',
        }
    )
    saved = forms.BooleanField(
        label='Запомнить',
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'id': 'saved',
                'checked': 'checked',
            })
    )

    def clean(self):
        try:
            user = User.objects.get(login=self.cleaned_data.get('user'))
        except User.DoesNotExist:
            self.add_error('user', 'Не верное имя пользователя')
            raise forms.ValidationError('Ошибка входа')
        else:
            if not user.activate:
                self.add_error('user', 'Не активированная запись')
                raise forms.ValidationError('Ошибка входа')
            else:
                secret = Secret.objects.get(user_id=user.id)
                hash_passwd = hash_user_pass(str(self.cleaned_data.get('password')), secret.sol)
                if user.hash_passwd != hash_passwd:
                    self.add_error('password', 'Не верный пароль')
                    raise forms.ValidationError('Ошибка входа')
                else:
                    self.cleaned_data['shadow_id'] = secret.shadow_id
        return self.cleaned_data


class EditUser(forms.Form):
    name = forms.CharField(
        max_length=50,
        label='Ваше имя',
        widget=forms.TextInput(
            attrs={
                'id': 'name',
            }),
        error_messages={
            'required': 'Введите Ваше имя'
        }
    )
    family = forms.CharField(
        max_length=50,
        label='Ваша фамилия',
        widget=forms.TextInput(
            attrs={
                'id': 'family',
            }),
        error_messages={
            'required': 'Введите Вашу фамилию'
        }
    )
    email = forms.CharField(
        max_length=50,
        label='Ваш email',
        widget=forms.EmailInput(
            attrs={
                'id': 'email',
            }),
        error_messages={
            'required': 'Введите Ваш email'
        }
    )
    telephone = forms.CharField(
        max_length=25,
        label='Ваш номер телефонa',
        widget=forms.TextInput(
            attrs={
                'id': 'telephone',
            }),
        error_messages={
            'required': 'Введите Ваш номер телефонa'
        }
    )
    country = forms.CharField(
        max_length=255,
        label='Страна',
        widget=forms.TextInput(
            attrs={
                'id': 'country',
                'class': 'custom_input',
            }),
        error_messages={
            'required': 'Введите Страну'
        }
    )
    region = forms.CharField(
        max_length=255,
        label='Регион / Область',
        widget=forms.TextInput(
            attrs={
                'id': 'region',
                'class': 'custom_input',
            }),
        error_messages={
            'required': 'Введите Регион / Область'
        }
    )
    district = forms.CharField(
        max_length=255,
        label='Район',
        widget=forms.TextInput(
            attrs={
                'id': 'district',
                'class': 'custom_input',
            }),
        error_messages={
            'required': 'Введите район'
        }
    )
    city = forms.CharField(
        max_length=255,
        label='Населенный пункт',
        widget=forms.TextInput(
            attrs={
                'id': 'city',
                'class': 'custom_input',
            }),
        error_messages={
            'required': 'Введите населенный пункт'
        }
    )
    street = forms.CharField(
        max_length=150,
        label='Улица, корпус, дом, квартира',
        widget=forms.TextInput(
            attrs={
                'id': 'street',
            }),
        error_messages={
            'required': 'Введите улицу, корпус, дом, квартиру'
        }
    )
    country_id = forms.IntegerField(
        widget=forms.HiddenInput(attrs={
            'id': 'country_id'
        }))
    region_id = forms.IntegerField(
        widget=forms.HiddenInput(attrs={
            'id': 'region_id'
        }))
    district_id = forms.IntegerField(
        widget=forms.HiddenInput(attrs={
            'id': 'district_id'
        }))
    city_id = forms.IntegerField(
        widget=forms.HiddenInput(attrs={
            'id': 'city_id'
        }))

    def save(self, id):
        User.objects.filter(id=int(id)).update(
            name=self.cleaned_data.get('name'),
            family=self.cleaned_data.get('family'),
            email=self.cleaned_data.get('email'),
            telephone=self.cleaned_data.get('telephone'),
            country_id=self.cleaned_data.get('country_id'),
            region_id=self.cleaned_data.get('region_id'),
            district_id=self.cleaned_data.get('district_id'),
            city_id=self.cleaned_data.get('city_id'),
            street=self.cleaned_data.get('street')
        )

    def clean(self):
        if not match(NAME, self.cleaned_data.get('name')):
            self.add_error('name', 'Допускаются русские, латинские символы и знак -')
            raise forms.ValidationError('Ошибка ввода')

        if not match(NAME, self.cleaned_data.get('family')):
            self.add_error('family', 'Допускаются русские, латинские символы и знак -')
            raise forms.ValidationError('Ошибка ввода')

        if not match(EMAIL, self.cleaned_data.get('email')):
            self.add_error('email', 'Email не соответствует шаблону')
            raise forms.ValidationError('Ошибка ввода')

        if not match(PHONE, self.cleaned_data.get('telephone')):
            self.add_error('telephone', 'Номер не соответствует шаблону')
            raise forms.ValidationError('Ошибка ввода')

        try:
            country = Country.objects.get(name_ru=self.cleaned_data.get('country'))
        except Country.DoesNotExist:
            self.add_error('country', 'Данной страны нет в базе данных')
            raise forms.ValidationError('Ошибка ввода')
        else:
            pass

        try:
            region = Region.objects.get(
                country_id=country.id,
                name_ru=self.cleaned_data.get('region')
            )
        except Region.DoesNotExist:
            self.add_error('region', 'Данного региона / области нет в базе данных')
            raise forms.ValidationError('Ошибка ввода')
        else:
            pass

        try:
            district = District.objects.get(
                region_id=region.id,
                name_ru=self.cleaned_data.get('district')
            )
        except District.DoesNotExist:
            self.add_error('district', 'Данного районного центра нет в базе данных')
            raise forms.ValidationError('Ошибка ввода')
        else:
            pass

        try:
            City.objects.get(
                district_id=district.id,
                name_ru=self.cleaned_data.get('city')
            )
        except City.DoesNotExist:
            self.add_error('city', 'Данного населенного пункта нет в базе данных')
            raise forms.ValidationError('Ошибка ввода')
        else:
            pass

        if not match(STREET, self.cleaned_data.get('street')):
            self.add_error('street', 'В названии можно использовать А-Яа-яA-Za-z- ,./')
            raise forms.ValidationError('Ошибка ввода')
        return self.cleaned_data


class NewPass(forms.Form):

    old_password = forms.CharField(
        max_length=50,
        label='Старый пароль',
        widget=forms.PasswordInput(
            attrs={
            }),
        error_messages={
            'required': 'Введите старый пароль'
        }
    )
    password = forms.CharField(
        max_length=50,
        label='Новай пароль',
        widget=forms.PasswordInput(
            attrs={
            }),
        error_messages={
            'required': 'Введите новый пароль'
        }
    )
    password_repeat = forms.CharField(
        max_length=50,
        label='Подтверждение пароля',
        widget=forms.PasswordInput(
            attrs={
            }),
        error_messages={
            'required': 'Введите подтверждение пароля'
        }
    )
    user_login = forms.CharField(widget=forms.HiddenInput())

    def save(self, id):
        user = User.objects.get(id=int(id))
        user.hash_passwd = self.cleaned_data.get('password')
        user.save()

    def clean(self):
        try:
            user = User.objects.get(login=self.cleaned_data.get('user_login'))
        except User.DoesNotExist:
            self.add_error('old_password', 'Не верный пароль')
            raise forms.ValidationError('Ошибка ввода')
        else:
            secret = Secret.objects.get(user_id=user.id)
            hash_passwd = hash_user_pass(str(self.cleaned_data.get('old_password')), secret.sol)
            if user.hash_passwd != hash_passwd:
                self.add_error('old_password', 'Не верный пароль')
                raise forms.ValidationError('Ошибка ввода')
            else:
                if not match(PASSWORD, self.cleaned_data.get('password')):
                    self.add_error('password', 'Слабый пароль')
                    raise forms.ValidationError('Ошибка ввода')
                if self.cleaned_data.get('password') != self.cleaned_data.get('password_repeat'):
                    self.add_error('password_repeat', 'Пароли не совподают')
                    raise forms.ValidationError('Ошибка ввода')
        return self.cleaned_data


class DeleteUser(forms.Form):
    password = forms.CharField(
        max_length=50,
        label='Ваш пароль',
        widget=forms.PasswordInput(
            attrs={
                'id': 'password',
            }),
        error_messages={
            'required': 'Введите Ваш пароль'
        }
    )
    user_login = forms.CharField(widget=forms.HiddenInput())

    def clean(self):
        try:
            user = User.objects.get(login=self.cleaned_data.get('user_login'))
        except User.DoesNotExist:
            self.add_error('password', 'Не верный пароль')
            raise forms.ValidationError('Ошибка ввода')
        else:
            secret = Secret.objects.get(user_id=user.id)
            hash_passwd = hash_user_pass(str(self.cleaned_data.get('password')), secret.sol)
            if user.hash_passwd != hash_passwd:
                self.add_error('password', 'Не верный пароль')
                raise forms.ValidationError('Ошибка ввода')
        return self.cleaned_data
