async function loadHTML(path) {
  // Load HTML from the specified path into the main #container div
  // The scroll is reset when doing this, so we have to save the scroll in tmp and set it back once the element is added.
  tmp = window.scrollY;
  document.getElementById("container").insertAdjacentHTML("beforeend", (await (await fetch(path)).text()).toString());
  window.scroll(0, tmp);

  // Additionally, stop the "Create PDF" button from being greyed out
  document.getElementById("create").removeAttribute("style");
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

  if (final_json.length !== 0) { // Only run if JSON exists`
    // Send data to backend via POST
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "data", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    var data = JSON.stringify(final_json);
    xhr.send(data);

    previousContent = document.getElementById("create").textContent; // Save previous content in order to reset
    document.getElementById("create").textContent = "Loading...";

    xhr.onload = () => {
      console.log(xhr.status)
      // Finally, add the "download PDF" button so that the user can download the result
      // But only add if the button doesn't already exist, and the XHR returned 201 (so a document has been created)
      if (document.getElementById("download") == null && xhr.status == 201) {
        code = `<a target="_blank" id="download" href="/download" class="inline-block float-right text-sm p-1.5 text-black font-medium">Download PDF</a>`
        document.getElementById("navbar").insertAdjacentHTML("beforeend", code)
      }

      document.getElementById("create").textContent = previousContent; // reset content
    }
  }
}

function removeElement() {
  // Remember to grey out "Create PDF" if all elements are gone.
}
