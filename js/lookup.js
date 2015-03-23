function addLookup(input) {
  var suggestionsList = document.createElement('datalist');
  var id = Math.floor(Number.MAX_SAFE_INTEGER * Math.random());
  var suggestionsCache = {};
  var titles = {};

  document.body.appendChild(suggestionsList);
  suggestionsList.id = 'suggestions-' + id;
  input.setAttribute('list', suggestionsList.id);

  function display(suggestions) {
    suggestionsList.textContent = '';

    for (var i = 0; i < suggestions.length; i++) {
      var suggestion = suggestions[i];
      var opt = document.createElement('option');

      opt.value = suggestion.Title + ' (' + suggestion.Year + ')';
      suggestionsList.appendChild(opt);
      titles[opt.value] = suggestion.imdbID;
    }
  }

  window['result$' + id] = function(k) {
    return function(data) {
      var suggestions = suggestionsCache[k] = data.Search || [];

      if (k == input.value.toLowerCase())
        display(suggestions);
    };
  }

  input.addEventListener('input', function(ev) {
    var k = input.value.toLowerCase().split(' (')[0];
    var suggestions = suggestionsCache[k];

    if (suggestions)
      display(suggestions)
    else {
      var scr = document.createElement('script');

      scr.src = 'http://www.omdbapi.com/?s=' + encodeURIComponent(k + '*') + '&callback=' + encodeURIComponent('result$' + id + '(' + JSON.stringify(k) + ')');
      document.body.appendChild(scr);
    }
  });

  return titles;
}
