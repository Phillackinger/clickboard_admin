# Clickboard Admin
Little Python programm for the Clickboard Administration built with PySimpleGuiQT and the python library of supbase

## Installation

You need a modern version of Python 3 (3.6-[3.7](https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64.exe)) in oder to run the programm.
If you havn't got Python installed you can donwload the installer from the [Officel Website](https://www.python.org/).
Before installing make sure you tick the `Add to Path` option at the opening screen of the installer.

Navigate to the folder with the source code and open a Terminal/Powersehll/CMD in this loaction.


```powershell
# Install the dependcies
pip install -r requierments.txt
# or run install.bat
```
before we can start the programm we need to specify our API-Key and URL in the `.env` file. If ther is none create one that looks like this.
```.env
SUPABASE_URL=
SUPABASE_KEY=
```

these variables are filled in without `"` or `'`

```powershell
# Run the app
python app.py
# or run start.bat
```

