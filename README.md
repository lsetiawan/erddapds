# erddapds
Tool for generating erddap datasets and integrate to datasets xml

Package Version | Erddap Version
---|---
0.1-alpha | 1.82

## Installing Master Version

Linux/OS X

```bash
wget https://raw.githubusercontent.com/lsetiawan/erddapds/master/requirements.txt
wget https://raw.githubusercontent.com/lsetiawan/erddapds/master/requirements-dev.txt
conda create -n erddapds -c conda-forge --yes python=3.6 --file requirements.txt --file requirements-dev.txt
source activate erddapds
pip install git+https://github.com/lsetiawan/erddapds.git
```