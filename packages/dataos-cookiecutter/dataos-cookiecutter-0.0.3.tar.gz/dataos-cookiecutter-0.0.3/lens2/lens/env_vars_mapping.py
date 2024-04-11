env_var_mappings = {
    "postgres": {
        "LENS2_DB_HOST": "LENS2_DB_HOST",
        "LENS2_DB_PORT": "LENS2_DB_PORT",
        "LENS2_DB_NAME": "LENS2_DB_NAME",
        "LENS2_DB_USER": "LENS2_DB_USER",
        "LENS2_DB_PASS": "LENS2_DB_PASS",
        "LENS2_DB_TYPE": "postgres"
    },
    "mysql": {
        "LENS2_DB_HOST": "LENS2_DB_HOST",
        "LENS2_DB_PORT": "LENS2_DB_PORT",
        "LENS2_DB_NAME": "LENS2_DB_NAME",
        "LENS2_DB_USER": "LENS2_DB_USER",
        "LENS2_DB_PASS": "LENS2_DB_PASS",
        "LENS2_DB_TYPE": "mysql"
    },
    "oracle": {
        "LENS2_DB_HOST": "LENS2_DB_HOST",
        "LENS2_DB_PORT": "LENS2_DB_PORT",
        "LENS2_DB_NAME": "LENS2_DB_NAME",
        "LENS2_DB_USER": "LENS2_DB_USER",
        "LENS2_DB_PASS": "LENS2_DB_PASS",
        "LENS2_DB_TYPE": "oracle"
    },
    "mssql": {
        "LENS2_DB_HOST": "LENS2_DB_HOST",
        "LENS2_DB_PORT": "LENS2_DB_PORT",
        "LENS2_DB_NAME": "LENS2_DB_NAME",
        "LENS2_DB_USER": "LENS2_DB_USER",
        "LENS2_DB_PASS": "LENS2_DB_PASS",
        "LENS2_DB_TYPE": "mssql"
    },
    "redshift": {
        "LENS2_DB_HOST": "LENS2_DB_HOST",
        "LENS2_DB_NAME": "LENS2_DB_NAME",
        "LENS2_DB_USER": "LENS2_DB_USER",
        "LENS2_DB_PASS": "LENS2_DB_PASS",
        "LENS2_DB_TYPE": "redshift"
    },
    'trino': {
        "LENS2_DB_HOST": "LENS2_DB_HOST",
        "LENS2_DB_PORT": "LENS2_DB_PORT",
        "LENS2_DB_USER": "LENS2_DB_USER",
        "LENS2_DB_PASS": "LENS2_DB_PASS",
        "LENS2_DB_PRESTO_CATALOG": "LENS2_DB_PRESTO_CATALOG",
        "LENS2_DB_SCHEMA": "LENS2_DB_SCHEMA",
        "LENS2_DB_TYPE": "trino"
    },
    "snowflake": {
        "CUBEJS_DB_SNOWFLAKE_ACCOUNT": "CUBEJS_DB_SNOWFLAKE_ACCOUNT",
        "CUBEJS_DB_SNOWFLAKE_WAREHOUSE": "CUBEJS_DB_SNOWFLAKE_WAREHOUSE",
        "CUBEJS_DB_NAME": "CUBEJS_DB_NAME",
        "CUBEJS_DB_USER": "CUBEJS_DB_USER",
        "CUBEJS_DB_PASS": "CUBEJS_DB_PASS",
        "CUBEJS_DB_TYPE": "snowflake"
    },
    "bigquery": {
        "CUBEJS_DB_BQ_PROJECT_ID": "CUBEJS_DB_BQ_PROJECT_ID",
        "CUBEJS_DB_BQ_KEY_FILE": "CUBEJS_DB_BQ_KEY_FILE",
        "CUBEJS_DB_BQ_CREDENTIALS": "CUBEJS_DB_BQ_CREDENTIALS",
        "CUBEJS_DB_TYPE": "bigquery"
    },
    "clickhouse": {
        "LENS2_DB_HOST": "LENS2_DB_HOST",
        "LENS2_DB_NAME": "LENS2_DB_NAME",
        "LENS2_DB_USER": "LENS2_DB_USER",
        "LENS2_DB_PASS": "LENS2_DB_PASS",
        "LENS2_DB_TYPE": "clickhouse"
    },
    "required": {
        "LENS2_NAME": f"{0}",
        "LENS2_DESCRIPTION": "lens description",
        "LENS2_TAGS": "'lens2 tags (comma separated)'",
        "LENS2_AUTHORS": "'lens2 auther names (comma separated)'"
    },
    "lens_other_config": {
        "LENS2_BASE_URL": "http://localhost:4000/lens2",
        "LENS2_META_PATH": "/v2/meta",
        "LENS2_DATAOS_USER_NAME": "dataos_user_name",
        "LENS2_DATAOS_USER_APIKEY": "dataos_user_apikey",
        "LENS2_RILL_PATH": "rill",
        "LENS2_CHECKS_PATH": "checks"
    }
}
