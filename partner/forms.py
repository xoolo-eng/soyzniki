from django import forms
from partner.models import Partner, Tariff, Point
from user.models import User, Secret
from re import compile, match
from soyzniki.models import Country, Region, District, City
from soyzniki.main.auth import hash_user_pass
from map.models import Services
from re import compile, match
from soyzniki.main.point_edge import add_utmost_coords


PHONE = compile('^(\s*)?(\+)?([- _():=+]?\d[- >():=+]?){10,14}(\s*)?$')
EMAIL = compile('^([\w]+)((.?|-?|_?)[\w]+)?@([\w-]{2,15}\.)+([\w]{2,6})$')
LOGIN = compile('^[a-zA-Z][a-zA-Z0-9-_\.]{3,25}$')
STREET = compile('^[а-яА-ЯёЁa-zA-Z0-9-_, \./]{3,150}$')
UNP_UNN = compile('[\d]{9,15}')


class FormPatrner(forms.Form):
    name = forms.CharField(
        max_length=255,
        label='Название организации',
        widget=forms.TextInput(attrs={
            'id': 'name'
        }),
        error_messages={
            'required': 'Поле "Название организации" обязательно для заролнения'
        })
    unp_unn = forms.CharField(
        max_length=255,
        label='УНН/УНП',
        widget=forms.TextInput(attrs={
            'id': 'unp_unn'
        }),
        error_messages={
            'required': 'Полу "УНН/УНП" обязательно к заролнению'
        })
    contact_person = forms.CharField(
        max_length=255,
        label='Контактное лицо',
        widget=forms.TextInput(attrs={
            'id': 'contact_person'
        }),
        error_messages={
            'required': 'Поле "Контактное лицо" обязательно к заполнению'
        })
    thelephones = forms.CharField(
        max_length=255,
        label='Телефоны',
        widget=forms.TextInput(attrs={
            'id': 'thelephones'
        }),
        error_messages={
            'required': 'Поле "Телефоны" обязательно к заполнению'
        })
    email = forms.CharField(
        max_length=255,
        label='Email',
        widget=forms.TextInput(attrs={
            'id': 'email'
        }),
        error_messages={
            'required': 'Поле "Email" обязательно к заполнению'
        })
    country = forms.CharField(
        max_length=255,
        label='Страна',
        widget=forms.TextInput(attrs={
            'class': 'custom_input',
            'id': 'country'
        }),
        error_messages={
            'required': 'Поле "Страна" обязательно к заполнению'
        })
    region = forms.CharField(
        max_length=255,
        label='Область/Регион',
        widget=forms.TextInput(attrs={
            'class': 'custom_input',
            'id': 'region'
        }),
        error_messages={
            'required': 'Поле "Область/Регион" обязательно к заполнению'
        })
    district = forms.CharField(
        max_length=255,
        label='Район',
        widget=forms.TextInput(attrs={
            'class': 'custom_input',
            'id': 'district'
        }),
        error_messages={
            'required': 'Поле "Район" обязательно к заполнению'
        })
    city = forms.CharField(
        max_length=255,
        label='Город',
        widget=forms.TextInput(attrs={
            'class': 'custom_input',
            'id': 'city'
        }),
        error_messages={
            'required': 'Поле "Город" обязательно к заполнению'
        })
    street = forms.CharField(
        max_length=255,
        label='Улица, дом',
        widget=forms.TextInput(attrs={
            'id': 'street'
        }),
        error_messages={
            'required': 'Поле "Улица, дом" обязательно к заполнению'
        })
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

    def save(self, user_id):
        user = User.objects.get(id=user_id)
        tariff = Tariff.objects.all()[0]
        new_partner = Partner()
        new_partner.name = self.cleaned_data.get('name')
        new_partner.unp_unn = self.cleaned_data.get('unp_unn')
        new_partner.contact_person = self.cleaned_data.get('contact_person')
        new_partner.thelephones = self.cleaned_data.get('thelephones')
        new_partner.email = self.cleaned_data.get('email')
        new_partner.street = self.cleaned_data.get('street')
        new_partner.country_id = self.cleaned_data.get('country_id')
        new_partner.region_id = self.cleaned_data.get('region_id')
        new_partner.district_id = self.cleaned_data.get('district_id')
        new_partner.city_id = self.cleaned_data.get('city_id')
        new_partner.tariff = tariff
        new_partner.save()
        new_partner.user.add(user)
        new_partner.save()

    def clean(self):
        try:
            Partner.objects.get(
                unp_unn=int(self.cleaned_data.get('unp_unn'))
            )
        except Partner.DoesNotExist:
            pass
        else:
            self.add_error('unp_unn', 'Организация с данным УНП/УНН уже зарегистрирована')
            raise forms.ValidationError('Исправте ошибки и повторите отправку формы')
        if not match(UNP_UNN, self.cleaned_data.get('unp_unn')):
            self.add_error('unp_unn', 'Допускаются только цифры')
            raise forms.ValidationError('Исправте ошибки и повторите отправку формы')

        if not match(EMAIL, self.cleaned_data.get('email')):
            self.add_error('email', 'Email не соответствует шаблону')
            raise forms.ValidationError('Исправте ошибки и повторите отправку формы')

        if not match(PHONE, self.cleaned_data.get('thelephones')):
            self.add_error('thelephones', 'Номер не соответствует шаблону')
            raise forms.ValidationError('Исправте ошибки и повторите отправку формы')

        try:
            Country.objects.get(id=self.cleaned_data.get('country_id'))
        except Country.DoesNotExist:
            self.add_error('country', 'Данной страны нет в базе данных')
            raise forms.ValidationError('Исправте ошибки и повторите отправку формы')

        try:
            region = Region.objects.get(
                id=self.cleaned_data.get('region_id')
            )
        except Region.DoesNotExist:
            self.add_error('region', 'Данного региона / области нет в базе данных')
            raise forms.ValidationError('Исправте ошибки и повторите отправку формы')
        else:
            if region.country_id != self.cleaned_data.get('country_id'):
                self.add_error('region', 'Ошибка идентификации региона')
                raise forms.ValidationError('Исправте ошибки и повторите отправку формы')

        try:
            district = District.objects.get(
                id=self.cleaned_data.get('district_id')
            )
        except District.DoesNotExist:
            self.add_error('district', 'Данного районного центра нет в базе данных')
            raise forms.ValidationError('Исправте ошибки и повторите отправку формы')
        else:
            if district.region_id != self.cleaned_data.get('region_id'):
                self.add_error('region', 'Ошибка идентификации района')
                raise forms.ValidationError('Исправте ошибки и повторите отправку формы')

        try:
            city = City.objects.get(
                id=self.cleaned_data.get('city_id')
            )
        except City.DoesNotExist:
            self.add_error('city', 'Данного населенного пункта нет в базе данных')
            raise forms.ValidationError('Исправте ошибки и повторите отправку формы')
        else:
            if city.district_id != self.cleaned_data.get('district_id'):
                self.add_error('region', 'Ошибка идентификации населенного пункта')
                raise forms.ValidationError('Исправте ошибки и повторите отправку формы')

        if not match(STREET, self.cleaned_data.get('street')):
            self.add_error('street', 'В названии можно использовать А-Яа-яA-Za-z- ,./')
            raise forms.ValidationError('Исправте ошибки и повторите отправку формы')

        return self.cleaned_data


class LoginSearch(forms.Form):
    login = forms.CharField(
        max_length=25,
        widget=forms.TextInput(
            attrs={
                'id': 'login',
                'style': 'display: inline',
            })
    )

    def clean(self):
        try:
            user = User.objects.get(login=self.cleaned_data.get('login'))
        except User.DoesNotExist:
            self.add_error('login', 'Пользователь в логином <{}> не найден'.format(
                self.cleaned_data.get('login')))
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class DataSearch(forms.Form):
    name = forms.CharField(
        required=False,
        max_length=50,
        label='Имя',
        widget=forms.TextInput(
            attrs={
                'id': 'name',
            })
    )
    family = forms.CharField(
        required=False,
        max_length=50,
        label='Фамилия',
        widget=forms.TextInput(
            attrs={
                'id': 'family',
            })
    )
    email = forms.CharField(
        required=False,
        max_length=50,
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'id': 'email',
            })
    )
    telephone = forms.CharField(
        required=False,
        max_length=25,
        label='номер телефонa',
        widget=forms.TextInput(
            attrs={
                'id': 'telephone',
            })
    )
    country = forms.CharField(
        max_length=255,
        required=False,
        label='Страна',
        widget=forms.TextInput(
            attrs={
                'id': 'country',
                'class': 'custom_input',
            })
    )
    region = forms.CharField(
        max_length=255,
        required=False,
        label='Регион / Область',
        widget=forms.TextInput(
            attrs={
                'id': 'region',
                'class': 'custom_input',
            })
    )
    district = forms.CharField(
        max_length=255,
        required=False,
        label='Район',
        widget=forms.TextInput(
            attrs={
                'id': 'district',
                'class': 'custom_input',
            })
    )
    city = forms.CharField(
        max_length=255,
        required=False,
        label='Населенный пункт',
        widget=forms.TextInput(
            attrs={
                'id': 'city',
                'class': 'custom_input',
            })
    )
    street = forms.CharField(
        required=False,
        max_length=150,
        label='Улица, корпус, дом, квартира',
        widget=forms.TextInput(
            attrs={
                'id': 'street',
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


class FormPatrnerEdit(forms.Form):
    contact_person = forms.CharField(
        max_length=255,
        label='Контактное лицо',
        widget=forms.TextInput(attrs={
            'id': 'contact_person'
        }),
        error_messages={
            'required': 'Поле "Контактное лицо" обязательно к заполнению'
        })
    thelephones = forms.CharField(
        max_length=255,
        label='Телефоны',
        widget=forms.TextInput(attrs={
            'id': 'thelephones'
        }),
        error_messages={
            'required': 'Поле "Телефоны" обязательно к заполнению'
        })
    email = forms.CharField(
        max_length=255,
        label='Email',
        widget=forms.TextInput(attrs={
            'id': 'email'
        }),
        error_messages={
            'required': 'Поле "Email" обязательно к заполнению'
        })
    country = forms.CharField(
        max_length=255,
        label='Страна',
        widget=forms.TextInput(attrs={
            'class': 'custom_input',
            'id': 'country'
        }),
        error_messages={
            'required': 'Поле "Страна" обязательно к заполнению'
        })
    region = forms.CharField(
        max_length=255,
        label='Область/Регион',
        widget=forms.TextInput(attrs={
            'class': 'custom_input',
            'id': 'region'
        }),
        error_messages={
            'required': 'Поле "Область/Регион" обязательно к заполнению'
        })
    district = forms.CharField(
        max_length=255,
        label='Район',
        widget=forms.TextInput(attrs={
            'class': 'custom_input',
            'id': 'district'
        }),
        error_messages={
            'required': 'Поле "Район" обязательно к заполнению'
        })
    city = forms.CharField(
        max_length=255,
        label='Город',
        widget=forms.TextInput(attrs={
            'class': 'custom_input',
            'id': 'city'
        }),
        error_messages={
            'required': 'Поле "Город" обязательно к заполнению'
        })
    street = forms.CharField(
        max_length=255,
        label='Улица, дом',
        widget=forms.TextInput(attrs={
            'id': 'street'
        }),
        error_messages={
            'required': 'Поле "Улица, дом" обязательно к заполнению'
        })
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

    def clean(self):
        if not match(EMAIL, self.cleaned_data.get('email')):
            self.add_error('email', 'Email не соответствует шаблону')
            raise forms.ValidationError('Исправте ошибки и повторите отправку формы')

        if not match(PHONE, self.cleaned_data.get('thelephones')):
            self.add_error('thelephones', 'Номер не соответствует шаблону')
            raise forms.ValidationError('Исправте ошибки и повторите отправку формы')

        try:
            Country.objects.get(id=self.cleaned_data.get('country_id'))
        except Country.DoesNotExist:
            self.add_error('country', 'Данной страны нет в базе данных')
            raise forms.ValidationError('Исправте ошибки и повторите отправку формы')

        try:
            region = Region.objects.get(
                id=self.cleaned_data.get('region_id')
            )
        except Region.DoesNotExist:
            self.add_error('region', 'Данного региона / области нет в базе данных')
            raise forms.ValidationError('Исправте ошибки и повторите отправку формы')
        else:
            if region.country_id != self.cleaned_data.get('country_id'):
                self.add_error('region', 'Ошибка идентификации региона')
                raise forms.ValidationError('Исправте ошибки и повторите отправку формы')

        try:
            district = District.objects.get(
                id=self.cleaned_data.get('district_id')
            )
        except District.DoesNotExist:
            self.add_error('district', 'Данного районного центра нет в базе данных')
            raise forms.ValidationError('Исправте ошибки и повторите отправку формы')
        else:
            if district.region_id != self.cleaned_data.get('region_id'):
                self.add_error('region', 'Ошибка идентификации района')
                raise forms.ValidationError('Исправте ошибки и повторите отправку формы')

        try:
            city = City.objects.get(
                id=self.cleaned_data.get('city_id')
            )
        except City.DoesNotExist:
            self.add_error('city', 'Данного населенного пункта нет в базе данных')
            raise forms.ValidationError('Исправте ошибки и повторите отправку формы')
        else:
            if city.district_id != self.cleaned_data.get('district_id'):
                self.add_error('region', 'Ошибка идентификации населенного пункта')
                raise forms.ValidationError('Исправте ошибки и повторите отправку формы')

        if not match(STREET, self.cleaned_data.get('street')):
            self.add_error('street', 'В названии можно использовать А-Яа-яA-Za-z- ,./')
            raise forms.ValidationError('Исправте ошибки и повторите отправку формы')

        return self.cleaned_data


class DelPartner(forms.Form):
    user_id = forms.IntegerField(
        widget=forms.HiddenInput()
    )
    password = forms.CharField(
        label='Пароль пользователя',
        widget=forms.PasswordInput()
    )

    def clean(self):
        try:
            user = User.objects.get(id=self.cleaned_data.get('user_id'))
            secret = Secret.objects.get(user_id=self.cleaned_data.get('user_id'))
        except User.DoesNotExist:
            self.add_error('password', 'Не верный пароль')
            raise forms.ValidationError('Ошибка ввода')
        else:
            if (user.hash_passwd != hash_user_pass(
                self.cleaned_data.get('password'),
                secret.sol
            )):
                self.add_error('password', 'Не верный пароль')
                raise forms.ValidationError('Ошибка ввода')
        return self.cleaned_data


'''
...............................................
..00000......0000....00..000.....00....0000....
..00..00...00....00......0000....00..00....00..
..00...00..00....00..00..00.00...00..00........
..00..00...00....00..00..00..00..00...000000...
..00000....00....00..00..00...00.00........00..
..00.......00....00..00..00....0000..00....00..
..00.........0000....00..00.....000....0000....
...............................................
'''
LAT_LON = compile('-?[\d]{1,3}\.[\d]{4,20}')
HTTP = compile('^http://')
HTTPS = compile('^https://')


class AddPoint(forms.ModelForm):
    country = forms.CharField(
        max_length=255,
        label='Страна',
        widget=forms.TextInput(attrs={
            'class': 'custom_input',
            'id': 'country'
        })
    )
    region = forms.CharField(
        max_length=255,
        label='Область/Регион',
        widget=forms.TextInput(attrs={
            'class': 'custom_input',
            'id': 'region'
        })
    )
    district = forms.CharField(
        max_length=255,
        label='Район',
        widget=forms.TextInput(attrs={
            'class': 'custom_input',
            'id': 'district'
        })
    )
    city = forms.CharField(
        max_length=255,
        label='Населенный пункт',
        widget=forms.TextInput(attrs={
            'class': 'custom_input',
            'id': 'city'
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
    time_work = forms.CharField(
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Point
        fields = '__all__'
        exclude = [
            'partner',
            'stock',
            'content_stock',
            'other_services',
            'active',
            'country',
            'region',
            'district',
            'city',
            'time_work',
        ]

    def save(self, partner_id):
        point = Point()
        point.partner_id = partner_id
        point.servis = self.cleaned_data.get('servis')
        point.name = self.cleaned_data.get('name')
        point.transport = self.cleaned_data.get('transport')
        point.country_id = self.cleaned_data.get('country_id')
        point.region_id = self.cleaned_data.get('region_id')
        point.district_id = self.cleaned_data.get('district_id')
        point.city_id = self.cleaned_data.get('city_id')
        point.street = self.cleaned_data.get('street')
        point.time_work = self.cleaned_data.get('time_work')
        point.thelephones = self.cleaned_data.get('thelephones')
        point.url = self.cleaned_data.get('url')
        point.desc = self.cleaned_data.get('desc')
        point.lat = self.cleaned_data.get('lat')
        point.lon = self.cleaned_data.get('lon')
        point.save()
        add_utmost_coords(self.cleaned_data.get('country_id'))

    def update(self, point_id):
        point = Point.objects.get(id=point_id)
        point.servis = self.cleaned_data.get('servis')
        point.name = self.cleaned_data.get('name')
        point.transport = self.cleaned_data.get('transport')
        point.country_id = self.cleaned_data.get('country_id')
        point.region_id = self.cleaned_data.get('region_id')
        point.district_id = self.cleaned_data.get('district_id')
        point.city_id = self.cleaned_data.get('city_id')
        point.street = self.cleaned_data.get('street')
        point.time_work = self.cleaned_data.get('time_work')
        point.thelephones = self.cleaned_data.get('thelephones')
        point.url = self.cleaned_data.get('url')
        point.desc = self.cleaned_data.get('desc')
        point.lat = self.cleaned_data.get('lat')
        point.lon = self.cleaned_data.get('lon')
        point.save()
        add_utmost_coords(self.cleaned_data.get('country_id'))

    def clean(self):
        from urllib.request import urlopen
        from urllib.error import URLError
        # проверка сервиса
        services = Services.objects.all()
        if self.cleaned_data.get('servis') not in services:
            self.add_error('servis', 'Такой услуги нет в списке')
            raise forms.ValidationError('Ошибка ввода')
        # проверка видов транспорта
        if (self.cleaned_data.get('transport') > 3 or
                self.cleaned_data.get('transport') < 1):
            self.add_error(
                'transport',
                'Такого вида танспорта нет в вписке'
            )
            raise forms.ValidationError('Ошибка ввода')
        # проверка url
        if not self.cleaned_data.get('url'):
            pass
        else:
            if (not match(HTTPS, self.cleaned_data.get('url')) and
                    not match(HTTP, self.cleaned_data.get('url'))):
                url = 'https://{}'.format(
                    self.cleaned_data.get('url')
                )
                try:
                    urlopen(url)
                except URLError:
                    url = 'http://{}'.format(
                        self.cleaned_data.get('url')
                    )
                    try:
                        urlopen(url)
                    except URLError:
                        self.add_error('url', 'Данный url не отвечает')
                        self.add_error('url', 'Проверьте введенное значение')
                        raise forms.ValidationError('Ошибка ввода')
                    else:
                        self.cleaned_data['url'] = url
                else:
                    self.cleaned_data['url'] = url
            else:
                try:
                    urlopen(self.cleaned_data.get('url'))
                except URLError:
                    self.add_error('url', 'Данный url не отвечает')
                    self.add_error('url', 'Проверьте введенное значение')
                    raise forms.ValidationError('Ошибка ввода')
        # проверка страны
        try:
            country = Country.objects.get(
                id=self.cleaned_data.get('country_id')
            )
        except Country.DoesNotExist:
            self.add_error('coutnry', 'Не верное значение, повторно введите адрес')
            raise forms.ValidationError('Ошибка ввода')
        else:
            if self.cleaned_data.get('country') != country.name_ru:
                self.add_error('coutnry', 'Не верное значение, повторно введите адрес')
                raise forms.ValidationError('Ошибка ввода')
        # проверка региона
        try:
            region = Region.objects.get(
                id=self.cleaned_data.get('region_id')
            )
        except Region.DoesNotExist:
            self.add_error('region', 'Не верное значение, повторно введите адрес')
            raise forms.ValidationError('Ошибка ввода')
        else:
            if self.cleaned_data.get('region') != region.name_ru:
                self.add_error('region', 'Не верное значение, повторно введите адрес')
                raise forms.ValidationError('Ошибка ввода')
            if region.country_id != self.cleaned_data.get('country_id'):
                self.add_error('region', 'Не верное значение, повторно введите адрес')
                raise forms.ValidationError('Ошибка ввода')
        # проверка района
        try:
            district = District.objects.get(
                id=self.cleaned_data.get('district_id')
            )
        except District.DoesNotExist:
            self.add_error('district', 'Не верное значение, повторно введите адрес')
            raise forms.ValidationError('Ошибка ввода')
        else:
            if self.cleaned_data.get('district') != district.name_ru:
                self.add_error('district', 'Не верное значение, повторно введите адрес')
                raise forms.ValidationError('Ошибка ввода')
            if district.region_id != self.cleaned_data.get('region_id'):
                self.add_error('district', 'Не верное значение, повторно введите адрес')
                raise forms.ValidationError('Ошибка ввода')
        # проверка населенного пункта
        try:
            city = City.objects.get(
                id=self.cleaned_data.get('city_id')
            )
        except City.DoesNotExist:
            self.add_error('city', 'Не верное значение, повторно введите адрес')
            raise forms.ValidationError('Ошибка ввода')
        else:
            if self.cleaned_data.get('city') != city.name_ru:
                self.add_error('city', 'Не верное значение, повторно введите адрес')
                raise forms.ValidationError('Ошибка ввода')
            if city.district_id != self.cleaned_data.get('district_id'):
                self.add_error('city', 'Не верное значение, повторно введите адрес')
                raise forms.ValidationError('Ошибка ввода')
        # проверка координат
        if not match(LAT_LON, self.cleaned_data.get('lat')):
            self.add_error('lat', 'Не корректное значение')
            self.add_error('lat', 'Повторно выберите точку на крте')
            raise forms.ValidationError('Ошибка ввода')
        if not match(LAT_LON, self.cleaned_data.get('lon')):
            self.add_error('lon', 'Не корректное значение')
            self.add_error('lon', 'Повторно выберите точку на крте')
            raise forms.ValidationError('Ошибка ввода')
        return self.cleaned_data
