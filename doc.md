# Basic layer structure
Data flows through these layers sequentially.
| Layer name | Layer function                                                |
| ---------- | ------------------------------------------------------------- |
| UI         | Input and interface creation                                  |
| Submission | JavaScript compilation to JSON format                         |
| Backend    | Modify JSON as appropriate                                    |
| Compilation| Compile JSON to LaTeX etc using preamble and defined commands |

# Details
## Configuration file
This file is read from by all other layers. It stores information for buckets, elements and the entire document. The format is:
```json
{
  "elements": {
    <name in elements/ directory>: {
      "bucket": <appropriate bucket>,
      "fields": {
        <id (that will be used in HTML and in compilation)>: {
          "type": <short-input, long-input, short-dropdown, long-dropdown, textarea>,
          "options": <for dropdowns> ["a", "b", ...]
        }
      },
      "function": <this is what the field will be compiled to. Uses $<fieldname> for string replacement> "\latexfunc{$name}{$content}"
    }
  },
  "buckets": {
    <bucket name>: {
      "begin": <text added at beginning of bucket>,
      "end": <text added at end of bucket>,
      "persistent": <bool: if false, begin and end text disappears if the bucket is empty; if true, they remain>
    }
  },
  "document": {
    "template-source": <source of preamble document which contains any template text and the string formatting locations of buckets>,
    "write-location": <file compilation layer should write to>
    "compilation-command": <command to compile the file, if necessary (e.g. for LaTeX),
    "document-source": <source where final document is found, if different from write-location>
  }
}
```

## UI layer
### Interface
When the program is run, the program must create the UI elements to be put in the elements/ directory. It does this by reading the "fields" attribute for each element in the config and compiling the appropriate fields into the HTML.

### Input
UI input is populated using the navigation bar, which reads HTML from the elements/ directory and whose content is also based on this directory. Actions like removing and adding elements are abstracted to the JavaScript in this layer.

An important feature of this layer is the ability for elements to be added and removed based on input (e.g. a dropdown activating a text input if the user selects "other".)

## Submission layer
Once the "Create PDF" button is presssed, this layer activates. It iterates through the current elements in the #container div and converts them to this JSON format:
```json
{
  "type": <name in elements/ directory e.g. "point">,
  "values": {
    <id of input>: <value of input>,
  }
}
```

This is then passed to the backend layer.

## Backend layer
This layer handles all the logic of the program. It is responsible for adding the `bucket` attribute to all of the JSON elements, depending on their `type`. It can also change the data before compilation (e.g., sorting elements or escaping characters for different languages.) The output of each element looks like:
```json
{
  "type": etc
  ...
  "bucket": <appropriate bucket, from config>,
  "function": <appropriate function, from config>
}
```

## Compilation layer
### Functions
Each element in the passed JSON will be converted into the appropriate text using the `function` attribute. This attribute uses "$<fieldname>" syntax for string replacement. Then the functions are added to the appropriate buckets.

### Buckets
Each function is prescribed a bucket by the Backenc layer via the "bucket" attribute in the config. The functions are added to their appropriate bucket in the order they are found (so sorting should be done in the backend.) Each bucket also has begin and end text that is added conditionally.

Once each bucket has its content, they are then added to the document itself (write-location in the config.) Then, if `compilation-command` exists, it is run. The compilation layer then ends, prompting the backend to read the file at write-source, or document-source if it exists, and make this available to the frontend via the /download post request.
