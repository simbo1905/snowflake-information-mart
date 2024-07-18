#!/usr/bin/env python3

import subprocess
import json
import os
import yaml
import argparse
from dotenv import load_dotenv

def run_command(command, env=None, log_output=True):
    """Run a shell command and return the output."""
    print(f"Running command: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        print(f"Error running command: {command}")
        print(result.stderr)
        exit(1)
    if log_output:    
        print(result.stdout)
    return result.stdout

def load_yaml_files(directory):
    """Load YAML files from the specified directory into environment variables."""
    yaml_vars = {}
    for filename in os.listdir(directory):
        if filename.endswith(('.yaml', '.yml')):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                yaml_content = file.read()
                yaml_vars[filename] = yaml_content
    return yaml_vars

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Data Tools Script")
    parser.add_argument("-I", "--interactive", action="store_true", help="Run in interactive mode")
    return parser.parse_args()

def main():
    args = parse_arguments()

    # Check if secret.env file exists
    if not os.path.exists('secret.env'):
        print("Error: secret.env file not found. Please create a file containing settings for TF_VAR_snowflake_user, TF_VAR_snowflake_account, and TF_VAR_snowflake_password.")
        exit(1)

    # Load environment variables from secret.env
    load_dotenv('secret.env')
    env = os.environ.copy()

    required_vars = ['TF_VAR_snowflake_user', 'TF_VAR_snowflake_account', 'TF_VAR_snowflake_password']
    missing_vars = [var for var in required_vars if var not in env or not env[var]]

    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}. Please ensure these are set in the secret.env file.")
        exit(1)

    # Load YAML files from entities subfolder
    entities_dir = 'entities'
    if not os.path.exists(entities_dir):
        print(f"Error: {entities_dir} directory not found. Please create it and add your YAML files.")
        exit(1)

    yaml_vars = load_yaml_files(entities_dir)
    env.update(yaml_vars)

    # Step 1: Run dbt compile with updated environment variables
    print("Running dbt compile...")
    run_command("dbt compile --profiles-dir .", env=env)

    # Step 2: Run terraform plan and output to a plan file
    print("Running terraform plan...")
    plan_output = run_command("terraform plan -out=tfplan", env=env)

    # Step 3: Check the plan for changes or destroy actions
    print("Checking terraform plan for changes...")
    show_plan_output = run_command("terraform show -json tfplan", env=env, log_output=False)
    plan_json = json.loads(show_plan_output)

    changes = False
    destroy = False

    for resource_change in plan_json.get("resource_changes", []):
        if resource_change["change"]["actions"] != ["no-op"]:
            changes = True
            if "delete" in resource_change["change"]["actions"]:
                destroy = True

    # Step 4: Determine whether to apply changes
    should_apply = False

    if not changes:
        print("No changes detected in the terraform plan.")
    else:
        print("Changes detected in the terraform plan:")
        for resource_change in plan_json.get("resource_changes", []):
            actions = resource_change["change"]["actions"]
            if actions != ["no-op"]:
                print(f"Resource: {resource_change['address']}, Actions: {actions}")

        if destroy:
            print("Warning: The plan includes resource deletions.")

        if args.interactive:
            user_input = input("Do you want to apply these changes? (yes/no): ").strip().lower()
            should_apply = user_input == "yes"
        else:
            print("Running in non-interactive mode. Changes will be applied automatically.")
            should_apply = True

    # Step 5: Apply changes if necessary
    if should_apply:
        print("Applying changes...")
        run_command("terraform apply tfplan", env=env)

if __name__ == "__main__":
    main()
