# Snowflake Infomation Mart

DBT with Terraform for Snowflake.

First set a demo db

```sql
-- Create database
CREATE DATABASE DEMO_MART;

```

Next create the necessary env vars for tf to login in a file `secret.env`:

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
pip install -r requirements.txt
# This must output Core not Cloud:
dbt --version
```

Then use `dbt debug` to ensure you have a working profile.

You must then init the local statefile for the first time!

```shell
terraform apply -lock=false
```

From now on you can run dbt compile then terraform plan and apply using the helper script:

```shell
source dbt-env/bin/activate
./data-tools.py  
```

## TODO

- [X] Create a static table using a yaml file for columns.
- [X] Create a dynamic table using dbt templating. 
- [ ] Create a historised snapshot of a table using stream and task.
