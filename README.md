# image-exif

Dataloop FaaS example for a function that extracts image exif information and uploads it to item's metadata.

## SDK Installation

You need to have dtlpy installed, if don't already, install it by running:

```bash
pip install dtlpy --upgrade
```

## Usage

### CLI

```bash
cd <this directory>

dlp projects checkout --project-name <name of the project>

dlp packages push --checkout

dlp packages deploy --checkout
```
### SDK

```python
import dtlpy as dl

#######################################
# define package name and get project #
#######################################
package_name = 'image-metadata-extractor'
project = dl.projects.get(project_name='MyProject')

################
# push package #
################

# create module
module = dl.PackageModule(
    functions=[
        dl.PackageFunction(
            inputs=[
                dl.FunctionIO(
                    type=dl.PackageInputType.ITEM,
                    name='item'
                )
            ]
        )
    ]
)

# push package
package = project.packages.push(package_name=package_name,
                                modules=[module],
                                src_path='/image-metadata-extractor')

##################
# deploy service #
##################
service = package.services.deploy(service_name=package_name,
                                  runtime={'gpu': False,
                                           'numReplicas': 1,
                                           'concurrency': 100})

##################
# create trigger #
##################
filters = {'metadata': {'system': {'mimetype': 'image/*'}}}
trigger = service.triggers.create(name=package_name,
                                  filters=filters,
                                  actions=['Created'],
                                  execution_mode='Once',
                                  resource='Item')
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
