
from selectable.base import LookupBase
from selectable.registry import registry

from tschercha.query import suggestions, \
                            SEARCH_DIRECTION_DEU_RUM, \
                            SEARCH_DIRECTION_RUM_DEU, \
                            IDIOM_VALLADER, \
                            IDIOM_PUTER

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

registry.register(LookupDeuVal)
registry.register(LookupValDeu)
registry.register(LookupBidirVal)

registry.register(LookupDeuPut)
registry.register(LookupPutDeu)
registry.register(LookupBidirPut)