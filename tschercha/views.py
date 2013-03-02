#
# coding=utf-8

# http://devdoodles.wordpress.com/2009/02/16/user-authentication-with-django-registration/
# http://docs.b-list.org/django-registration/0.8/quickstart.html

import sqlite3, os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django import forms
from django.utils.html import escape
from django.utils.http import urlquote

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
    term = forms.CharField(max_length=100, required=False)
    idiom = forms.ChoiceField(choices=IDIOM_NAMES.items())
                  
def search(data):
    idiom = data["idiom"]
    if idiom == IDIOM_PUTER:
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
                           # de, beugungen, geschl, bereich 
                                            # rum, geschl, bereich.
    cursor.execute("SELECT m, tt, ww, ii,   n, ll, rr FROM dicziunari WHERE m LIKE ? OR n LIKE ? LIMIT 0, ?",
                   ("%%%s%%" % query, "%%%s%%" % query, limit))
    rows = cursor.fetchall()
    res = []
    for row in rows:
        keys = [(u'wort',       u'',  u'' ),
                (u'beugung',    u'',  u'' ),
                (u'geschlecht', u'{', u'}'),
                (u'bereich',    u'[', u']'),
                (u'pled',       u'',  u'' ),
                (u'gener',      u'{', u'}'),
                (u'chomp',      u'[', u']'),]
        def fmt(out, key, inp):
            inp = inp.strip()
            if inp is not None and len(inp) > 0:
                txt = u'<span class="%s">%s%s%s</span>' % (key[0], key[1], escape(inp), key[2])
                if key[0] in [u'wort', u'pled']:
                    # TODO regex "cf. auch: vergleichen" (low prio - only 5 words)
                    p = inp.find(u'cf. ')
                    if p != -1:
                        newTerm = inp[p+3:].strip()
                        # We should generate the relative path by our app url part
                        # and not hard-code it here
                        txt = '<a class="xref" href="/tschercha/?idiom=%s&term=%s">%s</a>' % \
                               (IDIOM_NAMES[idiom], urlquote(newTerm), txt)
                    else:
                        cbTxt = inp.replace("\"", "")
                        txt = '<a class="clipb" href=\'javascript:clipb("%s")\'>%s</a>' % (cbTxt, txt)
                out.append(txt)
                    
        de = []
        rum = []
        for i in range(4):
            fmt(de, keys[i], row[i])
        for i in range(4, len(row)):
            fmt(rum, keys[i], row[i])
        res.append((" ".join(de), " ".join(rum)))
        
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

