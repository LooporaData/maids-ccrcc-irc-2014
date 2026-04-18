# Code templates for build_* scripts

### Manifest
* `maids.handlebars` - Main Handlebars template for `handlebars.js`
  ```
    # To compile a new version, edit this file and run:
    handlebars ./code/templates/maids.handlebars -f ./docs/js/hbmaids.js

    # Or, define a new template entirely.
  ```
* `maids.html` - HTML template, used by `./code/build_html/xml2html.py`

