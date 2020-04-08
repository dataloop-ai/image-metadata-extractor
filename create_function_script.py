"""
If you use the CLI to automatically push and deploy the function
with the package.json and service.json, you do not need this file,
simply run the following commands in the shell:

cd <this directory>
dlp projects checkout --project-name <name of the project>
dlp packages push --checkout
dlp packages deploy --checkout


However, if you wish to use the SDK you can run the following script.
"""
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
    functions=dl.PackageFunction(
        inputs=dl.FunctionIO(
            type=dl.PackageInputType.ITEM, name='item')))

# push package
package = project.packages.push(package_name=package_name,
                                modules=module,
                                src_path='/Users/aharonlouzon/Desktop/Dataloop/image-metadata-extractor')

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
