# erddapds
Tool for generating erddap datasets and integrate to datasets xml

Adapted from https://bitbucket.org/salishsea/erddap-datasets, specially its [ERDDAP_datasets.ipynb jupyter notebook](http://nbviewer.jupyter.org/urls/bitbucket.org/salishsea/erddap-datasets/raw/tip/ERDDAP_datasets.ipynb)

Package Version | Erddap Version
---|---
0.1a0 | 1.82

## Installing Master Version

Linux/OS X

```bash
wget https://raw.githubusercontent.com/lsetiawan/erddapds/master/requirements.txt
wget https://raw.githubusercontent.com/lsetiawan/erddapds/master/requirements-dev.txt
conda create -n erddapds -c conda-forge --yes python=3.6 --file requirements.txt --file requirements-dev.txt
source activate erddapds
pip install git+https://github.com/lsetiawan/erddapds.git
```

## Usage Example

```python
In [1]: from erddapds import ERDDAPDATASET

In [2]: details = {'type': 'Timeseries', 'title': 'OOI Data NcFile', 'summary': 'OOI Testing Summary', 'fileNameRegex': 'OOI_CE02SHSM.nc'}

In [3]: edd = ERDDAPDATASET('OOI_CE02SHSM', details=details, variables={})

In [4]: tree = edd.generate_datasetxml('EDDTableFromNcCFFiles', '/home/erddap/testnc', 'OOI_CE02SHSM.nc', '', '', '', '', '', '', '', 'http://example.com', 'UW-APL', 'This is OOI Data!', 'OOI NetCDF', gds
   ...: _loc='/home/erddap/tomcat8/webapps/deverddap/WEB-INF/GenerateDatasetsXml.sh', big_parent_directory='/home/erddap/extra')
Dataset template sucessfully generated. See: /home/erddap/extra/logs/GenerateDatasetsXml.out

In [5]: edd.add_to_datasetsxml(dsxml='/home/erddap/tomcat8/content/erddap/datasets.xml')
['touch', '/home/erddap/extra/flag/OOI_CE02SHSM']
Dataset sucessfully added.
```
