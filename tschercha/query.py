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

import sqlite3, os
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
IDIOM_GRISCHUN = '2'
IDIOM_DEFAULT  = IDIOM_VALLADER
IDIOM_NAMES_T = ((IDIOM_VALLADER, 'Vallader'),
                 (IDIOM_PUTER,    'Puter'),
                 (IDIOM_GRISCHUN, 'Grischun')
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

global dbVallader, dbPuter, dbGrischun
dbVallader = None
dbPuter    = None
dbGrischun = None
def openDb(idiom):
    global dbVallader, dbPuter, dbGrischun
    if idiom == IDIOM_PUTER:
        db = dbPuter
    if idiom == IDIOM_GRISCHUN:
        db = dbGrischun
    else:
        db = dbVallader
    if db is not None:
        return db
    
    if idiom == IDIOM_PUTER:
        dbPath = "database/Puter.db"
    if idiom == IDIOM_GRISCHUN:
        dbPath = "database/Grischun.db"
    else:
        dbPath = "database/Vallader.db"
    
    print "Loading", dbPath
    
    dbPath = os.path.join(os.path.dirname(__file__), dbPath)
    db = sqlite3.connect(dbPath)
    cur = db.cursor()
    cur.execute("PRAGMA synchronous = OFF")
    cur.execute("PRAGMA temp_store = MEMORY")
    cur.execute("PRAGMA cache_size = 50000")

    if idiom == IDIOM_PUTER:
        dbPuter = db
    if idiom == IDIOM_GRISCHUN:
        dbGrischun = db
    else:
        dbVallader = db
    
    return db

def sqlLikeWithSearchMode(mode, query):
    if mode == SEARCH_MODE_EXACT:
        return "%s" % query
    elif mode == SEARCH_MODE_START:
        return "%s%%" % query
    elif mode == SEARCH_MODE_END:
        return "%%%s" % query
    return "%%%s%%" % query


def search(data):
        
    idiom     = data["idiom"]
    mode      = data["mode"]
    direction = data["direction"]

    if len(data["term"]) > 0:
        query = data["term"]
    else:
        return []
    
    limit = 200
    likeStr = sqlLikeWithSearchMode(mode, query)
    if IDIOM_GRISCHUN:
        keys = [(u'wort',       u'',  u'' ),
                (u'geschl',     u'{', u'}'),
                (u'anmerk',     u'[', u']'),
                (u'pled',       u'',  u'' ),
                (u'gener',      u'{', u'}'),
                (u'annot',      u'[', u']'),]
        cols = 'wort, geschl, anmerk, pled, gener, annot'
        splitIdx = 3
    else:
        keys = [(u'wort',       u'',  u'' ),
                (u'beug',       u'',  u'' ),
                (u'geschl',     u'{', u'}'),
                (u'anmerk',     u'[', u']'),
                (u'pled',       u'',  u'' ),
                (u'gener',      u'{', u'}'),
                (u'annot',      u'[', u']'),]
        cols = 'wort, beug, geschl, anmerk, pled, gener, annot'
        splitIdx = 4
    if direction == SEARCH_DIRECTION_BI_DIR:
        sql = "SELECT %s FROM dicziunari WHERE wort LIKE ? OR pled LIKE ? LIMIT 0, ?"
        sqlData = (likeStr, likeStr, limit)
    elif direction == SEARCH_DIRECTION_DEU_RUM:
        sql = "SELECT %s FROM dicziunari WHERE wort LIKE ? LIMIT 0, ?"
        sqlData = (likeStr, limit)
    elif direction == SEARCH_DIRECTION_RUM_DEU:
        sql = "SELECT %s FROM dicziunari WHERE pled LIKE ? LIMIT 0, ?"
        sqlData = (likeStr, limit)
        
    cursor = openDb(idiom).cursor()
    cursor.execute(sql % cols, sqlData)
    rows = cursor.fetchall()
    res = []
 
    for row in rows:
        def fmt(out, key, inp):
            if inp is not None:
                inp = inp.strip()
                if len(inp) > 0:
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
        for i in range(splitIdx):
            fmt(de, keys[i], row[i])
        for i in range(splitIdx, len(row)):
            fmt(rum, keys[i], row[i])
        res.append((" ".join(de), " ".join(rum)))
        
    return res

def suggestions(idiom, direction, term, limit=20):
    
    if len(term) == 0:
        return []
    
    cursor = openDb(idiom).cursor()

    likeStr = "%s%%" % term

    if direction == SEARCH_DIRECTION_DEU_RUM:
        cursor.execute("SELECT wort FROM dicziunari WHERE wort LIKE ? GROUP BY wort LIMIT 0, ?",
                       (likeStr, limit))
    else: #if direction == SEARCH_DIRECTION_RUM_DEU:
        cursor.execute("SELECT pled FROM dicziunari WHERE pled LIKE ? GROUP BY pled LIMIT 0, ?",
                       (likeStr, limit))
        
    rows = cursor.fetchall()
    rows = [r[0] for r in rows]
    return rows
