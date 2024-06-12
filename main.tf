terraform {
  backend "local" {
    path = "terraform.tfstate"
  }
}

terraform {
  required_providers {
    snowflake = {
      source = "Snowflake-Labs/snowflake"
      version = "~> 0.87"
    }
  }
}

provider "snowflake" {
  account  = var.snowflake_account
  user = var.snowflake_user
  password = var.snowflake_password
  role     = "ACCOUNTADMIN"
}

resource "snowflake_schema" "sources_schema" {
  database = "DEMO_MART"
  name     = "SOURCES"
  comment  = "Schema for source data"
}