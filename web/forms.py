from django import forms

# para que se muestre como un input de tipo date


class DateInput(forms.DateInput):
    input_type = 'date'


class ClienteForm(forms.Form):
    SEXO_CHOICES = (('M', 'Masculino'), ('F', 'Femenino'),
                    ('O', 'Otro')
                    )  # tupla de tuplas

    cedula = forms.CharField(label='Cedula', max_length=13)
    nombre = forms.CharField(label='Nombre', max_length=200, required=True)
    apellido = forms.CharField(label='Apellido', max_length=200, required=True)
    telefono = forms.CharField(label='Telefono', max_length=20)
    # el widget es para que se muestre como un textarea
    direccion = forms.CharField(label='Direccion', widget=forms.Textarea)
    email = forms.EmailField(label='Correo Electronico', max_length=150)
    sexo = forms.ChoiceField(label='Sexo', choices=SEXO_CHOICES)
    fecha_nacimiento = forms.DateField(
        label='Fecha de Nacimiento', input_formats=['%Y-%m-%d'], widget=DateInput())
