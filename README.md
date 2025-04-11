# Area Coverage Planning

This repository contains the Python3 translation of `AreaCoveragePlanning` repository of Paula Betriu.

## Initial set-up

After cloning the repository, you will need to setup a Python virtual environment and install all the dependencies.

If you are using PyCharm or another similar IDE, it will auto-setup the virtual environment for you.
if you are cloning this repo in a server (without IDE), follow this steps:

```shell
# Install Python
sudo apt update
sudo apt install -y python3 python3-venv

# Generate a virtual environment and activate it
python3 -m venv venv
source venv/bin/activate

# Install python requirements
pip install --upgrade pip
pip install -r requirements.txt
```

> The repository `pySPICElib` from Manel Soria will be installed directly as a python package.
> You do not need to clone it; just import it directly: `from pySPICElib import kernelFetch`

## Executing scripts

You can execute scripts either from the IDE's own "Run/Debug Configurations" tool, or manually from terminal.
In any case, *the scripts should be executed from the repo's root directory*.
If you are using the IDE to launch the scripts, make sure the `working directory` is set to this repo root dir.

## Test scripts

The folder `testing` provides with a bunch of scripts to test & validate several of the functions of this repo.
