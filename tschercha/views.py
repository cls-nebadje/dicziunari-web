#
# coding=utf-8

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
                            IDIOM_DEFAULT, IDIOM_NAMES, IDIOM_NAMES_T, \
                            SEARCH_MODE_DEFAULT, SEARCH_MODE_NAMES_T, \
                            SEARCH_DIRECTION_DEFAULT, SEARCH_DIRECTION_NAMES_T,\
    IDIOM_VALLADER, SEARCH_DIRECTION_DEU_RUM, SEARCH_DIRECTION_RUM_DEU

from tschercha.lookups import LookupDeuVal, LookupValDeu, LookupBidirVal, \
                              LookupDeuPut, LookupPutDeu, LookupBidirPut

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
    
def formForIdiomAndDirection(idiom, direction):
    if idiom == IDIOM_VALLADER:
        if direction == SEARCH_DIRECTION_RUM_DEU:
            return SearchFormValDeu
        elif direction == SEARCH_DIRECTION_DEU_RUM:
            return SearchFormDeuVal
        else:
            return SearchFormVal
    else:
        if direction == SEARCH_DIRECTION_RUM_DEU:
            return SearchFormPutDeu
        elif direction == SEARCH_DIRECTION_DEU_RUM:
            return SearchFormDeuPut
        else:
            return SearchFormPut
        
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

