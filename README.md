pip install virtualenv

python -m virtualenv env

env/scripts/activate

pip install -r requirements.txt

setup.py file creating for package creation

__init__ Indicates that this file is package

python setup.py install -- This creates or add or trates src and other folders as packages in the env

artifacts - \configuration of components(Data ingestion,Data transformation, Model training) which tells that from which side data came, path of data and its output is called or stored in Artifacts 

Our code -> Package -> pypi repo -> deleted using pip package manager This is created using setup.py file

Kubernetes helps to manage the container of the docker

utils.py --> Common functions that are used frequently in code written in this file