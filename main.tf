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

# create the a table in the public schema
resource "snowflake_table" "table" {
  database = "DEMO_MART"
  schema   = "PUBLIC"
  name     = "DEMO_TABLE"
  dynamic "column" {
    for_each = yamldecode(file("${path.module}/DEMO_TABLE.yaml"))["columns"]
    content {
      name = column.value["name"]
      type = column.value["type"]
    }
  }
}