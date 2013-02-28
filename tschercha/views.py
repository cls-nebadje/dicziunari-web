#
# coding=utf-8

# http://devdoodles.wordpress.com/2009/02/16/user-authentication-with-django-registration/
# http://docs.b-list.org/django-registration/0.8/quickstart.html
# http://jagdeepmalhi.blogspot.ch/2010/09/django-application-contact-form.html

import sqlite3, os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django import forms

class SearchForm(forms.Form):
    term = forms.CharField(max_length=100)
    puter = forms.BooleanField(required=False)
    
def search(data):
    if data["puter"]:
        dbPath = "database/Puter.db"
    else:
        dbPath = "database/Vallader.db"
    dbPath = os.path.join(os.path.dirname(__file__), dbPath)
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    
    query = data["term"]
    sql = "SELECT m, n FROM dicziunari WHERE m LIKE '%%%s%%' OR n LIKE '%%%s%%'" % (query, query)
    cursor.execute(sql)
    res = cursor.fetchall()

    return res
    
@login_required
def tschercha(request):
    result = []
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            result = search(form.cleaned_data)
    else:
        form = SearchForm()

    return render(request, 'tschercha.html',
                  {'form': form, 'result':result,})

