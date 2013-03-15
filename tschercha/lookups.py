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

from selectable.base import LookupBase
from selectable.registry import registry

from tschercha.query import suggestions, \
                            SEARCH_DIRECTION_DEU_RUM, \
                            SEARCH_DIRECTION_RUM_DEU, \
                            IDIOM_VALLADER, \
                            IDIOM_PUTER, IDIOM_GRISCHUN

class LookupDeuVal(LookupBase):
    def get_query(self, request, term):
        return suggestions(idiom=IDIOM_VALLADER,
                           direction=SEARCH_DIRECTION_DEU_RUM,
                           term=term,
                           limit=10)

class LookupValDeu(LookupBase):
    def get_query(self, request, term):
        return suggestions(idiom=IDIOM_VALLADER,
                           direction=SEARCH_DIRECTION_RUM_DEU,
                           term=term,
                           limit=10)

class LookupBidirVal(LookupBase):
    def get_query(self, request, term):
        suggRum = suggestions(idiom=IDIOM_VALLADER,
                              direction=SEARCH_DIRECTION_RUM_DEU,
                              term=term,
                              limit=7)
        suggDeu = suggestions(idiom=IDIOM_VALLADER,
                              direction=SEARCH_DIRECTION_DEU_RUM,
                              term=term,
                              limit=7)
        sugg = suggRum + suggDeu
        sugg.sort()
        return sugg

class LookupDeuPut(LookupBase):
    def get_query(self, request, term):
        return suggestions(idiom=IDIOM_PUTER,
                           direction=SEARCH_DIRECTION_DEU_RUM,
                           term=term,
                           limit=10)

class LookupPutDeu(LookupBase):
    def get_query(self, request, term):
        return suggestions(idiom=IDIOM_PUTER,
                           direction=SEARCH_DIRECTION_RUM_DEU,
                           term=term,
                           limit=10)

class LookupBidirPut(LookupBase):
    def get_query(self, request, term):
        suggRum = suggestions(idiom=IDIOM_PUTER,
                           direction=SEARCH_DIRECTION_RUM_DEU,
                           term=term,
                           limit=7)
        suggDeu = suggestions(idiom=IDIOM_PUTER,
                              direction=SEARCH_DIRECTION_DEU_RUM,
                              term=term,
                              limit=7)
        sugg = suggRum + suggDeu
        sugg.sort()
        return sugg

class LookupDeuGri(LookupBase):
    def get_query(self, request, term):
        return suggestions(idiom=IDIOM_GRISCHUN,
                           direction=SEARCH_DIRECTION_DEU_RUM,
                           term=term,
                           limit=10)

class LookupGriDeu(LookupBase):
    def get_query(self, request, term):
        return suggestions(idiom=IDIOM_GRISCHUN,
                           direction=SEARCH_DIRECTION_RUM_DEU,
                           term=term,
                           limit=10)

class LookupBidirGri(LookupBase):
    def get_query(self, request, term):
        suggRum = suggestions(idiom=IDIOM_GRISCHUN,
                           direction=SEARCH_DIRECTION_RUM_DEU,
                           term=term,
                           limit=7)
        suggDeu = suggestions(idiom=IDIOM_GRISCHUN,
                              direction=SEARCH_DIRECTION_DEU_RUM,
                              term=term,
                              limit=7)
        sugg = suggRum + suggDeu
        sugg.sort()
        return sugg

registry.register(LookupDeuVal)
registry.register(LookupValDeu)
registry.register(LookupBidirVal)

registry.register(LookupDeuPut)
registry.register(LookupPutDeu)
registry.register(LookupBidirPut)

registry.register(LookupDeuGri)
registry.register(LookupGriDeu)
registry.register(LookupBidirGri)
