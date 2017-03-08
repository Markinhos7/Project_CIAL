from django import forms
import datetime
from datetime import datetime , timedelta

class ReporteForm(forms.Form):
        OPTIONS = (
                ("Paillaco", "Paillaco"),
                ("Los angeles", "Los angeles"),
                ("Empalme Hinca Tco", "Empalme Hinca Tco"),
                ("Renaico", "Renaico"),
                ("Tranapuente", "Tranapuente"),
                ("Pto saavedra", "Pto saavedra"),

                )
        obra = forms.ChoiceField(label="Obra   ",widget=forms.Select(attrs={'class':'selector'}),
                                             choices=OPTIONS)
class EntelForm(forms.Form):
        
        day = forms.DateField()