current_id = 1; // ID for newly added elements

// Functions to remove or add styling that greys out and disables the "Create PDF" button
function disableCreateButton() { document.getElementById("create").classList.add("disabled"); }
function enableCreateButton()  { document.getElementById("create").classList.remove("disabled");  }

function parseInputToJSON() {
  // Parses the current input on the page into a JSON string that can be passed to the backend or validated by the frontend.
  // Collect data by iterating through all children of the container (the form elements)
  final_json = [];
  let form_elements = Array.from(document.getElementById("container").children);

  for (var i = 0; i < form_elements.length; i++) {
    element = form_elements[i];
    values = {};
    for (var i2 = 0; i2 < element.length; i2++) {
      values[element[i2].id] = element[i2].value;
    }

    final_json.push({ 'type': element.getAttribute("data-eltype"), 'values': values });
  }

  return final_json
}

function prevalidateJSON(json) {
  // A preliminary check to see whether the `json` provided *should* compile. Checks:
  // - Whether the JSON is blank, or:
  // - Whether all fields in the JSON are blank.
  // Returns false if invalid, true otherwise
  // Implicitly disables the create button if the JSON is invalid.
  valid = false;
  if (json == []) { valid = false; }
  else {
    // If the JSON is not blank, check if all the fields are blank.
    for (i = 0; i < json.length; i++) {
      values = json[i]['values']
      console.log(values)
      if (!(Object.values(values).every(v => v == ''))) { // If all fields aren't blank
        valid = true;
      }
    }

    if (!valid) { disableCreateButton(); } // The Create Button should always be disabled if the current JSON will not parse.
  }

  return valid;
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
      // Finally, add the "download PDF" button so that the user can download the result
      // But only add if the button doesn't already exist, and the XHR returned 201 (so a document has been created)
      if (xhr.status == 201) {
        document.getElementById("download").classList.remove("hidden");
      }
      else if (xhr.status !== 201) {
        alert("Something went wrong. Please check all fields are filled and try again.");
      }

      document.getElementById("create").textContent = previousContent; // reset content
    }
  } else {
    alert("Your input is empty. Please enter something and try again.")
  }
}

async function loadHTML(path) {
  // Each new element added needs an ID
  // Load HTML from the specified path into the main #container div. This is called by onclick() properties to add elements.
  // The scroll is reset when doing this, so we have to save the scroll in tmp and set it back once the element is added.
  tmp = window.scrollY;
  new_element = document.getElementById("container").insertAdjacentHTML("beforeend",
    (await (await fetch(path)).text()).toString().replaceAll("IDENT", current_id.toString()));
  window.scroll(0, tmp); // Set the scroll back now that the element has been added (this will reset scroll velocity but it's not a big concern)

  current_id += 1;
}

function removeElement(id) {
  // Remember to grey out "Create PDF" if all elements are gone.
  // Will call disableCreateButton()
  document.getElementById(id.toString()).remove();

  prevalidateJSON(parseInputToJSON()) // This will disable the create button if we just removed the last element.
}

// Input listener for disabling or undisabling the create button.
document.addEventListener("input", event => {
  if (event.data != null) { // If something was added and not removed
    enableCreateButton(); // If the user has inputted *something*, the button should be enabled.
  // Check if the JSON is now empty/invalid if something was removed (data is null):
  // (prevalidateJSON() will implicitly disable the button for us.)
  } else { prevalidateJSON(parseInputToJSON()) }
})
