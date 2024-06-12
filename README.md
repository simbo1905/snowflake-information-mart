# Snowflake Infomation Mart

DBT with Terraform for Snowflake.

First set a demo db

```sql
-- Create database
CREATE DATABASE DEMO_MART;

-- you may want to set the default wh to suspect after 60s
ALTER WAREHOUSE COMPUTE_WH SET AUTO_SUSPEND = 60;
```

Next create the necessary env vars for tf to login in a file `secret.env`:

```shell
export SNOWFLAKE_USER="you"
export SNOWFLAKE_PASSWORD="password"

# use role orgadmin; show organization accounts; 
# look at the account_locator_url and use the first three parts. for example:
# https://aq60000.uk-south.azure.snowflakecomputing.com
# would mean you have to set aq60000.uk-south.azure
export SNOWFLAKE_ACCOUNT="aq68616.uk-south.azure"


# terraform need them in a different format
export TF_VAR_snowflake_account="$SNOWFLAKE_ACCOUNT"
export TF_VAR_snowflake_user="$SNOWFLAKE_USER"
export TF_VAR_snowflake_password="$SNOWFLAKE_PASSWORD"

# customise these defaults for dbt which you can override by model or folder.
export SNOWFLAKE_ROLE=ACCOUNTADMIN
export SNOWFLAKE_WAREHOUSE=COMPUTE_WH
export SNOWFLAKE_DATABASE=DEMO_DB
export SNOWFLAKE_SCHEMA=PUBLIC
```

Note you must `source secret.env` to set these in our shell. 

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

Then use `dbt debug --profiles-dir .` to ensure you have a working profile.

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
