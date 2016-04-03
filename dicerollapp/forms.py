from django import forms

class NewDiceroll(forms.Form):
    description = forms.CharField(label='Description', max_length=100)


class NewRoll(forms.Form):
    dicenum = forms.IntegerField(label='Number of dices')