# Sources

Sources directory contains source reference databases, schemas, and tables in the database from which dbt can read data. They are defined within YAML files and referenced throughout model creation.

Instead of having to reference a data location in every script or model, sources allow you to name and define it once using your sources.yml file. 