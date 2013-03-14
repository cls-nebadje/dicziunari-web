/*
 * Dicziunari-Web -- Webserver backend for a multi-idiom Rhaeto-Romance
 *                   online dictionary.
 * 
 * Copyright (C) 2012-2013 Uli Franke (cls) et al.
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * 
 * IMPORTANT NOTICE: All software, content, intellectual property coming
 * with this program (usually contained in files) can not be used in any
 * way by the Lia Rumantscha (www.liarumantscha.ch/) without explicit
 * permission, as they actively block software innovation targeting the
 * Rhaeto-Romance language.
 *
 */

function qualifyURL(url) {
	var a = document.createElement('a');
	a.href = url;
	return a.href;
}

function installSearchEngine(engine) {
	if (window.external && ("AddSearchProvider" in window.external)) {
		// Firefox 2 and IE 7, OpenSearch
		window.external.AddSearchProvider(qualifyURL(engine));
	} else {
		// No search engine support (IE 6, Opera, etc).
		alert("Ingün sustegn per maschinas da tscherchar.");
	}
}

function installSearchEnginePuter() {
	/* Had to use non-template style relative address. Hope we don't change the
	 * static file path.
	 */
	installSearchEngine("/static/search-plugin-puter.xml");
}

function installSearchEngineVallader() {
	/* Had to use non-template style relative address. Hope we don't change the
	 * static file path.
	 */
	installSearchEngine("/static/search-plugin-vallader.xml");
}

function installSearchEngines() {
	installSearchEngineVallader();
	installSearchEnginePuter();
}

function clipb (text) {
	window.prompt ("Copchar alla memoria d'immez: Ctrl+C, Enter/Esc", text);
}

