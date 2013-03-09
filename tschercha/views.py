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

def nameToId(default, namedict):
    def convert(name):
        ident = default
        tmp = name.lower()
        for i, n in namedict.items():
            if tmp == n.lower():
                ident = i
                break
        return ident
    return convert

IDIOM_VALLADER = '0'
IDIOM_PUTER    = '1'
IDIOM_DEFAULT  = IDIOM_VALLADER
IDIOM_NAMES_T = ((IDIOM_VALLADER, 'Vallader'),
                 (IDIOM_PUTER,    'Puter'),
                 )
IDIOM_NAMES = dict(IDIOM_NAMES_T)
idiomNameToIdiom = nameToId(IDIOM_DEFAULT, IDIOM_NAMES)

SEARCH_MODE_LIBERAL = '0'
SEARCH_MODE_EXACT   = '1'
SEARCH_MODE_START   = '2'
SEARCH_MODE_END     = '3'
SEARCH_MODE_DEFAULT = SEARCH_MODE_LIBERAL

SEARCH_MODE_NAMES_T = ((SEARCH_MODE_LIBERAL, "Liberal"),
                       (SEARCH_MODE_EXACT,   "Exact"),
                       (SEARCH_MODE_START,   "Cumanzamaint"),
                       (SEARCH_MODE_END,     "Finischun"),
                       )
SEARCH_MODE_NAMES = dict(SEARCH_MODE_NAMES_T)
searchModeNameToSearchMode = nameToId(SEARCH_MODE_DEFAULT, SEARCH_MODE_NAMES)

SEARCH_DIRECTION_BI_DIR  = '0'
SEARCH_DIRECTION_DEU_RUM = '1'
SEARCH_DIRECTION_RUM_DEU = '2'
SEARCH_DIRECTION_DEFAULT = SEARCH_DIRECTION_BI_DIR
SEARCH_DIRECTION_NAMES_T = ((SEARCH_DIRECTION_BI_DIR, 'Bidirecziunal'),
                            (SEARCH_DIRECTION_DEU_RUM, 'Tudais-ch-Rumantsch'),
                            (SEARCH_DIRECTION_RUM_DEU, 'Rumantsch-Tudais-ch'),
                            )
SEARCH_DIRECTION_NAMES = dict(SEARCH_DIRECTION_NAMES_T)
searchDirNameToSearchDir = nameToId(SEARCH_DIRECTION_DEFAULT, SEARCH_DIRECTION_NAMES)

class SearchForm(forms.Form):
    term = forms.CharField(max_length=100, required=False)
    mode = forms.ChoiceField(choices=SEARCH_MODE_NAMES_T, label="Möd")
    direction = forms.ChoiceField(choices=SEARCH_DIRECTION_NAMES_T, label="Direcziun")
    idiom = forms.ChoiceField(choices=IDIOM_NAMES.items())
    
@login_required
def tschercha(request):
    result = []
    idiom = IDIOM_DEFAULT
    mode = SEARCH_MODE_DEFAULT
    direction = SEARCH_DIRECTION_DEFAULT
    
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            idiom = form.cleaned_data["idiom"]
            mode = form.cleaned_data["mode"]
            direction = form.cleaned_data["direction"]
            result = search(form.cleaned_data)
    else:
        idiom = idiomNameToIdiom(request.GET.get("idiom", ""))
        mode = searchModeNameToSearchMode(request.GET.get("mode", ""))
        direction = searchDirNameToSearchDir(request.GET.get("direcziun", ""))
        d = {"term"      : request.GET.get("term", ""),
             "idiom"     : idiom,
             "mode"      : mode,
             "direction" : direction,
             }
        result = search(d)
        form = SearchForm(initial=d)

    return render(request,
                  'tschercha.html',
                  {'form': form,
                   'result':result,
                   'idiom' : IDIOM_NAMES[idiom]})

def sqlLikeWithSearchMode(mode, query):
    if mode == SEARCH_MODE_EXACT:
        return "%s" % query
    elif mode == SEARCH_MODE_START:
        return "%s%%" % query
    elif mode == SEARCH_MODE_END:
        return "%%%s" % query
    return "%%%s%%" % query

def search(data):
    idiom = data["idiom"]
    mode = data["mode"]
    direction = data["direction"]
    print mode
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
    likeStr = sqlLikeWithSearchMode(mode, query)
    if direction == SEARCH_DIRECTION_BI_DIR:
                               # de, beugungen, geschl, bereich 
                                                # rum, geschl, bereich.
        cursor.execute("SELECT m, tt, ww, ii,   n, ll, rr FROM dicziunari WHERE m LIKE ? OR n LIKE ? LIMIT 0, ?",
                       (likeStr, likeStr, limit))
    elif direction == SEARCH_DIRECTION_DEU_RUM:
        cursor.execute("SELECT m, tt, ww, ii,   n, ll, rr FROM dicziunari WHERE m LIKE ? LIMIT 0, ?",
                       (likeStr, limit))
    elif direction == SEARCH_DIRECTION_RUM_DEU:
        cursor.execute("SELECT m, tt, ww, ii,   n, ll, rr FROM dicziunari WHERE n LIKE ? LIMIT 0, ?",
                       (likeStr, limit))
        
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
