async function loadHTML(path) {
  // Load HTML from the specified path into the main #container div
  // The scroll is reset when doing this, so we have to save the scroll in tmp and set it back once the element is added.
  tmp = window.scrollY;
  document.getElementById("container").insertAdjacentHTML("beforeend", (await (await fetch(path)).text()).toString());
  window.scroll(0, tmp);
}

// Get data from all form elements and send to backend using a POST request
function postData() {
  // Collect data by iterating through all children of the container (the form elements)
  final_json = [];
  let form_elements = Array.from(document.getElementById("container").children);

  for (var i = 0; i < form_elements.length; i++) {
    element = form_elements[i];
    values = [];
    for (var i2 = 0; i2 < element.length; i2++) {
      values.push(element[i2].value);
    }
    final_json.push({ 'type': element.id, 'values': values });
  }

  // Send data to backend via POST
  var xhr = new XMLHttpRequest();
  var url = "data";
  xhr.open("POST", url, true);
  xhr.setRequestHeader("Content-Type", "application/json");
  var data = JSON.stringify(final_json);
  xhr.send(data);

  // Finally, add the "download PDF" button so that the user can download the result
  // But only add if the button doesn't already exist.
  if (document.getElementById("download") == null) {
    code = `<a target="_blank" id="download" href="/download" class="inline-block float-right text-sm p-1.5 text-black font-medium">Download PDF</a>`
    document.getElementById("navbar").insertAdjacentHTML("beforeend", code)
  }
}
