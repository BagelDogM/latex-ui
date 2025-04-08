// TODO
// 1. (DONE) Make scroll not reset when adding new content - probably have to save it
// 2. Need to detect lists
// 3. replace \n with \newline but keep \n\n
// 4. Detect lists and add \begin{enumerate}
// 5. Ability to remove elements
// 6. Add conclusions/customise place/trial/visit conclusions
//
// 7. Add customisable inputs

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
}
