#
# coding=utf-8
#
# Dicziunari-Web -- Webserver backend for a multi-idiom Rhaeto-Romance
#                   online dictionary.
# 
# Copyright (C) 2012-2013 Uli Franke (cls) et al.
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# IMPORTANT NOTICE: All software, content, intellectual property coming
# with this program (usually contained in files) can not be used in any
# way by the Lia Rumantscha (www.liarumantscha.ch/) without explicit
# permission, as they actively block software innovation targeting the
# Rhaeto-Romance language.

# http://devdoodles.wordpress.com/2009/02/16/user-authentication-with-django-registration/
# http://docs.b-list.org/django-registration/0.8/quickstart.html

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django import forms
import selectable.forms

from tschercha.query import search, \
                            idiomNameToIdiom, \
                            searchModeNameToSearchMode, \
                            searchDirNameToSearchDir, \
                            IDIOM_GRISCHUN, IDIOM_PUTER, \
                            IDIOM_DEFAULT, IDIOM_NAMES, IDIOM_NAMES_T, \
                            SEARCH_MODE_DEFAULT, SEARCH_MODE_NAMES_T, \
                            SEARCH_DIRECTION_DEFAULT, SEARCH_DIRECTION_NAMES_T, \
                            SEARCH_DIRECTION_DEU_RUM, SEARCH_DIRECTION_RUM_DEU

from tschercha.lookups import LookupDeuVal, LookupValDeu, LookupBidirVal, \
                              LookupDeuPut, LookupPutDeu, LookupBidirPut, \
                              LookupDeuGri, LookupGriDeu, LookupBidirGri

# Note: For each lookup we need a new form!
class SearchForm(forms.Form):
    term = forms.CharField(max_length=100, required=False)
    mode = forms.ChoiceField(choices=SEARCH_MODE_NAMES_T, label="Möd")
    direction = forms.ChoiceField(choices=SEARCH_DIRECTION_NAMES_T, label="Direcziun")
    idiom = forms.ChoiceField(choices=IDIOM_NAMES_T)

class SearchFormDeuVal(SearchForm):
    term = forms.CharField(max_length=100, widget=selectable.forms.AutoCompleteWidget(LookupDeuVal), required=False)
class SearchFormValDeu(SearchForm):
    term = forms.CharField(max_length=100, widget=selectable.forms.AutoCompleteWidget(LookupValDeu), required=False)
class SearchFormVal(SearchForm):
    term = forms.CharField(max_length=100, widget=selectable.forms.AutoCompleteWidget(LookupBidirVal), required=False)
    
class SearchFormDeuPut(SearchForm):
    term = forms.CharField(max_length=100, widget=selectable.forms.AutoCompleteWidget(LookupDeuPut), required=False)
class SearchFormPutDeu(SearchForm):
    term = forms.CharField(max_length=100, widget=selectable.forms.AutoCompleteWidget(LookupPutDeu), required=False)
class SearchFormPut(SearchForm):
    term = forms.CharField(max_length=100, widget=selectable.forms.AutoCompleteWidget(LookupBidirPut), required=False)

class SearchFormDeuGri(SearchForm):
    term = forms.CharField(max_length=100, widget=selectable.forms.AutoCompleteWidget(LookupDeuGri), required=False)
class SearchFormGriDeu(SearchForm):
    term = forms.CharField(max_length=100, widget=selectable.forms.AutoCompleteWidget(LookupGriDeu), required=False)
class SearchFormGri(SearchForm):
    term = forms.CharField(max_length=100, widget=selectable.forms.AutoCompleteWidget(LookupBidirGri), required=False)
    
def formForIdiomAndDirection(idiom, direction):
    if idiom == IDIOM_PUTER:
        if direction == SEARCH_DIRECTION_RUM_DEU:
            return SearchFormPutDeu
        elif direction == SEARCH_DIRECTION_DEU_RUM:
            return SearchFormDeuPut
        else:
            return SearchFormPut
    elif idiom == IDIOM_GRISCHUN:
        if direction == SEARCH_DIRECTION_RUM_DEU:
            return SearchFormGriDeu
        elif direction == SEARCH_DIRECTION_DEU_RUM:
            return SearchFormDeuGri
        else:
            return SearchFormGri
    else:
        if direction == SEARCH_DIRECTION_RUM_DEU:
            return SearchFormValDeu
        elif direction == SEARCH_DIRECTION_DEU_RUM:
            return SearchFormDeuVal
        else:
            return SearchFormVal
        
@login_required
def tschercha(request):

    term = u""
    idiom = IDIOM_DEFAULT
    mode = SEARCH_MODE_DEFAULT
    direction = SEARCH_DIRECTION_DEFAULT
    
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            term = form.cleaned_data["term"]
            idiom = form.cleaned_data["idiom"]
            mode = form.cleaned_data["mode"]
            direction = form.cleaned_data["direction"]
    else:
        term = request.GET.get("term", "")
        idiom = idiomNameToIdiom(request.GET.get("idiom", ""))
        mode = searchModeNameToSearchMode(request.GET.get("mode", ""))
        direction = searchDirNameToSearchDir(request.GET.get("direcziun", ""))
    
    d = {"term"      : term,
         "idiom"     : idiom,
         "mode"      : mode,
         "direction" : direction,
         }
    result = search(d)

    form = formForIdiomAndDirection(idiom, direction)(initial=d)

    return render(request,
                  'tschercha.html',
                  {'form'   : form,
                   'result' : result,
                   'idiom'  : IDIOM_NAMES[idiom],
                   'user'   : user(request),
                   })

def user(request):
    if hasattr(request, 'user'):
        return request.user.username
    return "anonim"

