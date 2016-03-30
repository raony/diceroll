from django.shortcuts import render, redirect
from dicerollapp.forms import NewDiceroll
from dicerollapp.models import DiceRoll

def home(request):
    form = NewDiceroll()
    if request.method == 'POST':
        form = NewDiceroll(request.POST)
        if form.is_valid():
            obj = DiceRoll.manager.create(form.cleaned_data['description'])
            return redirect('diceroll', id=unicode(obj.GUID))
    return render(request, 'diceroll/home.html', {'form' : form})

def diceroll(request, id):
    obj = DiceRoll.manager.get(id)
    return render(request, 'diceroll/diceroll.html', {'diceroll' : obj})