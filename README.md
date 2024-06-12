# Snowflake Infomation Mart

DBT with Terraform for Snowflake.

First set a demo db

```sql
-- Create database
CREATE DATABASE DEMO_MART;

```

Next create the necessary env vars to login with:

```shell
export TF_VAR_snowflake_user="you"
# you must set this:
export TF_VAR_snowflake_password="xxxx"
# use role orgadmin; show organization accounts; 
# look at the account_locator_url and use the first three parts. for example:
# https://aq60000.uk-south.azure.snowflakecomputing.com
# would mean you have to set aq60000.uk-south.azure
export TF_VAR_snowflake_account="your_account.cloue_region.cloud"
```

Setup Terraform with:

```shell
tfenv install 1.8.5
tfenv use 1.8.5
```

Setup dbt-core

```shell
brew install python
softwareupdate --install-rosetta
python3 -m venv dbt-env
source dbt-env/bin/activate
pip install dbt-core dbt-snowflake
# This must output Core not Cloud:
dbt --version
```

You need to setup your dbt-core profile with the same settings then compile the models with 

You must then init the local statefile for the first time!

```shell
terraform apply -lock=false
```
