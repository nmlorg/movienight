function json(url, callback) {
  var req = new XMLHttpRequest();

  req.open('GET', url, true);
  req.addEventListener('load', function(ev) {
    if (req.status == 200)
      callback(JSON.parse(req.responseText));
  });
  req.send();
}
