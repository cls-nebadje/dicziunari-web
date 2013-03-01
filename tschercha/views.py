#
# coding=utf-8

# http://devdoodles.wordpress.com/2009/02/16/user-authentication-with-django-registration/
# http://docs.b-list.org/django-registration/0.8/quickstart.html

import sqlite3, os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django import forms

IDIOM_VALLADER = '0'
IDIOM_PUTER    = '1'
IDIOM_DEFAULT  = IDIOM_VALLADER

IDIOM_NAMES = {IDIOM_VALLADER : 'Vallader',
               IDIOM_PUTER    : 'Puter',
               }

def idiomNameToIdiom(idiomName):
    idiom = IDIOM_DEFAULT
    tmp = idiomName.lower()
    for i, n in IDIOM_NAMES.items():
        if tmp == n.lower():
            idiom = i
            break
    return idiom

class SearchForm(forms.Form):
    term = forms.CharField(max_length=100)
    idiom = forms.ChoiceField(choices=IDIOM_NAMES.items())
                  
def search(data):
    if data["idiom"] == IDIOM_PUTER:
        dbPath = "database/Puter.db"
    else:
        dbPath = "database/Vallader.db"
    
    dbPath = os.path.join(os.path.dirname(__file__), dbPath)
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()

    if len(data["term"]) > 0:
        query = data["term"]
    else:
        return []
    
    limit = 200
    sql = "SELECT m, n FROM dicziunari WHERE m LIKE '%%%s%%' OR n LIKE '%%%s%%' LIMIT 0, %i" % (query, query, limit)
    cursor.execute(sql)
    res = cursor.fetchall()

    return res
    
@login_required
def tschercha(request):
    result = []
    idiom = IDIOM_DEFAULT
    
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            idiom = form.cleaned_data["idiom"]
            result = search(form.cleaned_data)
    else:
        idiom = idiomNameToIdiom(request.GET.get("idiom", ""))
        d = {"term"  : request.GET.get("term", ""),
             "idiom" : idiom}
        result = search(d)
        form = SearchForm(initial=d)

    return render(request,
                  'tschercha.html',
                  {'form': form,
                   'result':result,
                   'idiom' : IDIOM_NAMES[idiom]})

