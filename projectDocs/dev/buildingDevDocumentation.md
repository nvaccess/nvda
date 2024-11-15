Before building developer documentation, [create your developer environment](./createDevEnvironment.md).

### Building developer documentation

To generate the NVDA developer guide, type:

```cmd
scons developerGuide
```

The developer guide will be placed in the `devDocs` folder in the output directory.

To generate the HTML-based source code documentation, type:

```cmd
scons devDocs
```

The documentation will be placed in the `NVDA` folder in the output directory.

### Building nvdaHelper developer documentation

To generate developer documentation for nvdaHelper (not included in the devDocs target):

```
scons devDocs_nvdaHelper
```

The documentation will be placed in the folder `<projectRoot>\output\devDocs\nvdaHelper`.
This requires having Doxygen installed.
