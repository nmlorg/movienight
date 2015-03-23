function json(url, callback) {
  var req = new XMLHttpRequest();

  req.open('GET', url, true);
  req.addEventListener('load', function(ev) {
    if (req.status == 200)
      callback(JSON.parse(req.responseText));
  });
  req.send();
}


function put(url, data, callback) {
  if (!(data instanceof FormData)) {
    var formData = new FormData();

    for (var k in data)
      formData.append(k, data[k]);

    data = formData;
  }

  var req = new XMLHttpRequest();

  req.open('PUT', url, true);
  req.addEventListener('load', function(ev) {
    if (callback && (req.status == 200))
      callback(JSON.parse(req.responseText));
  });
  req.send(data);
}
