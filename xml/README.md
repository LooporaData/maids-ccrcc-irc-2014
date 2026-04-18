# XML

### Manifest
* `./xml/empty/` - Contains the empty/template XML files designed to capture all descriptive data required by the MAIDS specification.
* `./xml/example/` - An example of filled XML files and used to generate the example documents.
* `./xml/target/` - A special directory that, if it exists, will be used by the CI/CD pipeline to autogenerate various data and documents.

All MAIDS descriptions should have a `target` directory located in `./xml/` that describes the dataset as fully as possible. To create the `target` directory, simply copy the `empty` directory, rename it, and begin filling out the XML files. We are working on less error prone methods to do this initial task.

You can use this namespacing feature to create descriptive views/facets on the underlying dataset to highlight particular qualities, generate documents, and share them. However, the main and most complete description should be specified in `target`.

_NOTE: Faceted descriptions is a feature we would like to officially support but is likely to be a stretch goal._