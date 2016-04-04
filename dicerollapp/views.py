from django.shortcuts import render, redirect
from django.http import Http404
from dicerollapp import forms
from dicerollapp.models import DiceRoll, DiceRollManager

def home(request):
    form = forms.NewDiceroll()
    if request.method == 'POST':
        form = forms.NewDiceroll(request.POST)
        if form.is_valid():
            obj = DiceRollManager.get_manager().create(form.cleaned_data['description'])
            return redirect('diceroll', id=unicode(obj.GUID))
    return render(request, 'diceroll/home.html', {
        'form' : form,
        'rolls' : [DiceRollManager.get_manager().get(k) for k in
            DiceRollManager.get_manager().keys()]
    })

def diceroll(request, id):
    obj = DiceRollManager.get_manager().get(id)
    form = forms.NewRoll()
    if not obj:
        raise Http404

    if request.method == 'POST':
        form = forms.NewRoll(request.POST)
        if form.is_valid():
            obj.roll(form.cleaned_data['dicenum'])
            DiceRollManager.get_manager().save(obj)
            return redirect('diceroll', id=unicode(obj.GUID))

    return render(request, 'diceroll/diceroll.html', {'diceroll' : obj, 'form': form})