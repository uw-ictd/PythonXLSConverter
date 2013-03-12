This is a Python script that converts XLS(X) files into JSON form defs for ODK Survey.
The XLS(X) format is described [here](https://code.google.com/p/opendatakit/wiki/XLSForm2Docs).

Command line usage:
-------------------

You will need a 2.x verion of python and xlrd.
In a terminal something like this should work:

    apt-get install easy_install #This command assumes ubuntu
    easy_install pip
    pip install xlrd

This is the calling convention:

`xlsform2.py path_to_XLSForm output_path`

[There is some documention on the syntax available here](http://code.google.com/p/opendatakit/wiki/XLSForm2Docs)

Running the Django web interface:
---------------------------------

This repository includes code for a Djano web interface for doing online form conversions.
[There may be a version of it running here.](http://ec2-50-16-84-43.compute-1.amazonaws.com/xlsform/2/)

Once you've set up a Django server, follow these steps to setup the app:

0. Install xlrd (see above).

1. git clone this repo into your Djano directory (the one containing urls.py).

2. In your settings.py add "PythonXLSConverter" to INSTALLED_APPS

3. Add these lines to your urls.py:

```python
urlpatterns += [url(r'', include('PythonXLSConverter.urls'))]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
```
4. Copy the ODK Survey "default" folder into the static directory.
