### FEQoR API
This a Flask application that handles the backend for FEQoR API.

##### To Run this application in development

 - Make sure miniconda has been installed:
    ```
    $ wget -O miniconda_install.sh https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
    $ ./miniconda_install.sh
    ```

 - Create Anaconda enviromment:
    ```sh
    $ conda env create -f environment.yml
    export ENVIRONMENT=local|tst|stg|prd
    Note: default environment is local.
    ```

 - Activate your new virtual environment and source your environment variables:
    ```
    $ source activate feqor_api_env
    ```

 - Run the server:
    ```sh
    development:
    $ python runner.py
    production:
    run ./run.sh(scripts located in deployment folder)
    ```

    ##### API Endpoints
    -------------------------------------------------------------------------
 - ****API basic information:***

         -  Dev API Server: http:///
         -  Test API Server: http:///

