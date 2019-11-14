## pymagextractor

This branch is only used for ```ui_design```.

To clone this branch, use the following
```git clone -b develop https://github.com/hilman-dayo/pymagextractor.git```


The UI is designed using ```Qt Designer```.

After complete UI editing, the python file needs to be generated using
```pyside2-uic filename.ui -o filename.py```

At the moment only ```Workspace``` tab and ```Extractor``` tab is usable.

In ```Extractor``` tab only ```image extractor``` is functionable.

### Prerequisites

- Ubuntu/Debian

```pip install pyside2 toml pandas opencv-python```
