variable "snowflake_account" {
  description = "The Snowflake account locator"
  type        = string
}

variable "snowflake_user" {
  description = "The Snowflake user"
  type        = string
}

variable "snowflake_password" {
  description = "The Snowflake password"
  type        = string
  sensitive   = true
}