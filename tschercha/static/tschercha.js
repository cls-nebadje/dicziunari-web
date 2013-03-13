
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

