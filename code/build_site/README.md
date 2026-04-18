# Code to autogenerate an HTML Description

### Manifest
* `helperHandlebars.py` - Helper functions with JS datastructure templates for `xml2html.py` to build `index.html`.
* `helperXML.py` - Helper function to parse XML into a python dictionary object.
* `xml2html.py` - Convert XML description of a dataset to a single-page site in `./docs/`.
    * __NOTE__: Make sure the example breaks before logging an issue.
    ```
    # Get help
    python xml2html.py -h

    # Create an example site, this makes use of files in ./xml/example/
    python ./code/build_site/xml2html.py -eg example

    # Create real description by filling in xml files in ./xml/
    python ./code/build_site/xml2html.py

    # You can specify a custom template name if you've compiled a new template
    python ./code/build_site/xml2html.py -t my_new_template
    ```
