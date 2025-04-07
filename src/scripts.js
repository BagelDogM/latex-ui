// TODO
// 1. Need to detect lists
// 2. replace \n with \newline but keep \n\n
// 3. Detect lists and add \begin{enumerate}
// 4. Ability to remove elements
// 5. Add conclusions/customise place/trial/visit conclusions
//
// 6. Add customisable inputs

// Each function grabs its respective html element from the templates/ folder and then pushes it into the <body> of the document
async function createpoint() {document.body.insertAdjacentHTML("beforeend", (await (await fetch("templates/point.html")).text()).toString());}
async function createvisit() {document.body.insertAdjacentHTML("beforeend", (await (await fetch("templates/visit.html")).text()).toString());}
async function createtrial() {document.body.insertAdjacentHTML("beforeend", (await (await fetch("templates/trial.html")).text()).toString());}
async function createplace() {document.body.insertAdjacentHTML("beforeend", (await (await fetch("templates/place.html")).text()).toString());}
