# PyIAACSync

## Introduction
infrastructure-as-code tools such as Terraform and Palumi are gaining popularity and increasingly becoming neceessary to support the principles of Site Reliability Engineering (SRE). 

However, there are a couple of disadvantages in existing tools in the market:
- Terraform requires knowledge of golang to be able to sync assets
- Both Terraform and Palumi plugins can be quite complex for beginners to manage and maintain - As in 2023, Terraform plugins require modules to be built in golang
- In a shared environment, where some assets are being built manually while others are being built using automation, tools like Terraform Automation can fail if assets managed by automation are deleted

PyIAACSync provides a framework which allows software engineering teams getting into infrastructure-as-code to easily create and sync assets which they have defined in YAML spec files, in a polled manner (non-event driven). The infrastructue components can be `anything` (AWS asset, GCP asset, any SIEM detection rule) that can be:
    a. described in YAML files, and 
    b. can be read, created or deleted via API calls

Software engineers need to create the following to leverage `pyiaacsync`:
1. A folder (`iaac_sync_folder`) that contains the specs/configs for the infrastructure to create
2. A simple asset python file that contains a class describing the asset with the following `static` functions:
   - `validate`: to validate whether the spec/config that has been supplied in the 
   - `create`: to create the asset via the supplied spec/config
   - `delete`: to delete that has been supplied via the spec/config
   - `check`: to check whether the asset that has been deployed matches the spec/config aka `integrity check`. If not, the asset will be re-created
   - `update` (Optional): to be called to update an existing asset, eg when the configuration gets changed. If not defined for the assets , then the `delete` / `create` gets called.

Please see `Usage` section that describes the example in more detail

## Install

### via PyPI

```
python3 -m pip install pyiaacsync
```

### Manually
Install all necessary dependencies as follows:
```
python3 -m pip install -r requirements.txt
```

## Usage

### Structure
We will be using the example `example-fileasset` described in the `examples` folder of this repository. Users of this repo can use the files in the `examples` folder (especially `fileasset.py`) to build their own assets with `pyiaacsync.py`.

In this folder, we have the following objects:
- `exampleconf`: a folder which contains 3 spec/config files (1 file is in a subfolder) that describe what kind of file to create
- `fileasset.py`: A python file that contains the fileasset which defines how to `validate` the spec config file, `create` asset from the spec / config file, `delete` the existing asset created from the config file and also `check` if the the created asset is different from the config file
- `example.py`: the main script which will invoke the creation of assets using pyiaacsync conf file

Note that `pyiaacsync` also has an `args` option available in `__init__` which can be used to provide any additional optional 
parameters as a dict that can be used by the asset class. Uncomment the `random_args` set line in `example.py` to see how it can be used:
```
...
    random_args = {}
    ## uncomment line below to demonstrate how the random arguments can work
    #random_args = {'message': 'hello world'}
```

*Note*: An additional example has been added in folder called `example-fileasset-with-update` where the `fileassetwupd.py` is a python file which additionally includes the `update` method in the `FileAssetWithUpdate` class. The commands listed below also apply to files in this folder.

*Note*: By default, pyiaacsync will immediately stop syncing assets if there are unexpected errors. This can be over-ridden by setting `true` to `continue_sync_on_error` and specifying an error handler `callback_on_sync_error` which will execute the error handler and continue the processing of remaining assets after executing `callback_on_sync_error` method. An example of this is included in `example-fileasset-with-update`.

*Assumption*: Note that all sync, delete, create, update actions are currently performed once only from pyiaacsync. Any retries must be built in the asset python file

### Actions

#### init
The first steps is to execute `init` which will create a new state file `out-teststate.yaml`:
```
python3 example.py -a init
```

To force re-creation of the state file even if it exists (NOTE: Beware this will delete the existing state file!):
```
python3 example.py -a init -if
```

We can also specify an existing state file to use:
```
python3 example.py -a init -if -f /tmp/out-teststatefile.yaml
```

#### validate_configs

To validate the configs in the spec folder for all existing assets using the `validate` function defined in `fileasset.py` class:
```
python3 example.py -a validate_configs
```

#### sync

To sync the assets based on the spec/configs folder continuously - this will create the files as per the configs in the folder.

Any changes made to the files the next time will be reset.
```
python3 example.py -a sync
```

To sync the assets once only:
```
python3 example.py -a sync_once
```

#### delete_assets

To delete all existing assets (in this case, all files) and remove the assets from the state file:
```
python3 example.py -a delete_assets
```

## TODO
- Add unit testing
