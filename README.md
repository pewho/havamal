Havamal - Formater Tool : LDIF to CSV file
==========================================

Summary
-------

Havamal is a simple tool to convert a LDIF file to CSV. It embaarks a simple system to map source attribut to cols in the CSV.
It enable also the capability to ignore some attributes with this mapping.

If it's a multi values attribute, CSV output join each value with ", ".

Output CSV is comma separated; fully double quoted, and UTF-8 encoded. Header is present.


Requirements
------------

- Python 3.4+


Installation
------------

- With pip tool

```
>> git clone
>> cd ./havamal
>> pip install .

```

- With setuptools

```
>> git clone
>> cd ./havamal
>> python setup.py install
```


Usage
-----

- To convert an LDIF to CSV:
```
>> havamal <PATH_TO_LDIF_FILE> <CSV_OUTPUT_PATH> <PATH_TO_MAPPER_FILE>
```

- To generate a default mapping from an LDIF file:
```
havamal_generate_default_mapper <PATH_TO_LDIF_FILE> <PATH_TO_OUTPUT_MAPPER_FILE>
```

- Mapper file use the default python ConfigFile format : see more information [here](https://docs.python.org/3/library/configparser.html)


Licence
-------

MIT
