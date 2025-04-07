// Generates the HTML for a generic item with customisable title
function genericPoint(title) {
    return `<form class="m-2 p-2 bg-white rounded-sm ring-1 ring-black/5 w-3/4 min-w-100">
        <p class="text-xs inline-block float-right p-1.5 text-gray/700 font-light">${title}</p>
        <input class="text-sm ring-1 ring-black/11 rounded-sm p-1 m-1.5 w-1/3 min-w-40" type="text" placeholder="Title">
        <br>
        <textarea class="text-sm ring-1 ring-black/11 rounded-sm p-1 m-1.5 w-19/20 h-50"></textarea>
    </form>`;
}

async function createpoint() {document.body.insertAdjacentHTML("beforeend", (await (await fetch("templates/point.html")).text()).toString());}
async function createvisit() {document.body.insertAdjacentHTML("beforeend", (await (await fetch("templates/visit.html")).text()).toString());}
async function createtrial() {document.body.insertAdjacentHTML("beforeend", (await (await fetch("templates/trial.html")).text()).toString());}
async function createplace() {document.body.insertAdjacentHTML("beforeend", (await (await fetch("templates/place.html")).text()).toString());}


// function loadHTML(html_string) {
//   // Loads HTML
//   textFile = "tmp.html";
//   var data = new Blob([html_string], {type: 'text/plain'});

//   // If we are replacing a previously generated file we need to
//   // manually revoke the object URL to avoid memory leaks.
//   if (textFile !== null) {
//     window.URL.revokeObjectURL(textFile);
//   }

//   textFile = window.URL.createObjectURL(data);

//   $("#test").load(textFile, function (response, status, xhr) {
//     if (status == "error") {
//       console.log(msg + xhr.status + " " + xhr.statusText);
//     }
//   })
// }
