create_disabled_style = `pointer-events: none;color:grey;`;

function disableCreateButton() { document.getElementById("create").setAttribute("style", create_disabled_style); }

function enableCreateButton() { document.getElementById("create").removeAttribute("style");  }

function parseInputToJSON() {
  // Parses the current input on the page into a JSON string that can be passed to the backend or validated by the frontend.
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

  return final_json
}

function prevalidateJSON(json) {
  // A preliminary check to see whether the `json` provided *should* compile. Checks:
  // - Whether the JSON is blank, or:
  // - Whether all fields in the JSON are blank.
  // Returns false if invalid, true otherwise
  if (json == []) { return false; }
  else {
    // If the JSON is not blank, check if all the fields are blank.
    for (i = 0; i < json.length; i++) {
      values = json[i]['values']
      if (!(values.every(v => v == ''))) { // If all fields aren't blank
        return true;
      }
    }

    return false;
  }
}

// Get data from all form elements and send to backend using a POST request
function postData() {
  final_json = parseInputToJSON();

  if (prevalidateJSON(final_json)) { // Only run if JSON is valid (not entirely empty)
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

      else if (xhr.status !== 201) {
        alert("Something went wrong. Please check all fields are filled and try again.")
      }

      document.getElementById("create").textContent = previousContent; // reset content
    }
  } else {
    alert("Your input is empty. Please enter something and try again.")
    disableCreateButton();
  }
}

async function loadHTML(path) {
  // Load HTML from the specified path into the main #container div. This is called by onclick() properties to add elements.
  // The scroll is reset when doing this, so we have to save the scroll in tmp and set it back once the element is added.
  tmp = window.scrollY;
  document.getElementById("container").insertAdjacentHTML("beforeend", (await (await fetch(path)).text()).toString());
  window.scroll(0, tmp) // Set the scroll back now that the element has been added (this will reset scroll velocity but it's not a big concern)
}

function removeElement() {
  // Remember to grey out "Create PDF" if all elements are gone.
  // Will call disableCreateButton()
}

document.addEventListener("input", event => {
  if (event.data != null) {
    enableCreateButton(); // If the user has inputted *something*, the button should be enabled.
  } else if (!(prevalidateJSON(parseInputToJSON()))) { // If the prevalidation fails, it is empty so no PDF can be compiled.
    disableCreateButton();
  }
})
