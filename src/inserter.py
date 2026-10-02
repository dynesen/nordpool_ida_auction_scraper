import os
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from psycopg2.extras import execute_values



# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
PASSWORD = os.getenv("PASSWORD")

# ============================================================
# FORECAST CONFIGURATION
# ============================================================


FORECAST_CONFIG = {

    # ========================================================
    # POWER FLOW
    # ========================================================

    "fact_power_flow": {

        "fact_table": "fact_power_flow",

        "dimensions": {

            "dim_granularity_sk": {
                "table": "dim_granularity",
                "dimension_key": "dim_granularity_sk",
                "value_column": "granularity"
            },

            "dim_data_provider_sk": {
                "table": "dim_data_provider",
                "dimension_key": "dim_data_provider_sk",
                "value_column": "data_provider"
            },

            "dim_power_grid_from_sk": {
                "table": "dim_power_grid",
                "dimension_key": "dim_power_grid_sk",
                "value_column": "power_grid"
            },

            "dim_power_grid_to_sk": {
                "table": "dim_power_grid",
                "dimension_key": "dim_power_grid_sk",
                "value_column": "power_grid"
            },

            "dim_power_flow_type_sk": {
                "table": "dim_power_flow_type",
                "dimension_key": "dim_power_flow_type_sk",
                "value_column": "power_flow_type"
            },

            "dim_value_type_sk": {
                "table": "dim_value_type",
                "dimension_key": "dim_value_type_sk",
                "value_column": "value_type"
            },

            "dim_value_unit_sk": {
                "table": "dim_value_unit",
                "dimension_key": "dim_value_unit_sk",
                "value_column": "value_unit"
            }
        },

        "series_keys": [
            "datetime_begin",
            "dim_granularity_sk",
            "dim_data_provider_sk",
            "dim_power_grid_from_sk",
            "dim_power_grid_to_sk",
            "dim_power_flow_type_sk",
            "dim_value_type_sk",
            "dim_value_unit_sk"
        ],

        "insert_columns": [
            "datetime_begin",
            "dim_granularity_sk",
            "dim_data_provider_sk",
            "dim_power_grid_from_sk",
            "dim_power_grid_to_sk",
            "dim_power_flow_type_sk",
            "dim_value_type_sk",
            "fact_value",
            "dim_value_unit_sk"
        ]
    },

    # ========================================================
    # JAO CONSTRAINTS
    # ========================================================

    "fact_jao_constraints": {

        "fact_table": "fact_jao_constraints",

        "dimensions": {

            "dim_granularity_sk": {
                "table": "dim_granularity",
                "dimension_key": "dim_granularity_sk",
                "value_column": "granularity"
            },

            "dim_data_provider_sk": {
                "table": "dim_data_provider",
                "dimension_key": "dim_data_provider_sk",
                "value_column": "data_provider"
            },

            "dim_jao_power_grid_sk": {
                "table": "dim_jao_power_grid",
                "dimension_key": "dim_jao_power_grid_sk",
                "value_column": "jao_power_grid"
            },

            "dim_jao_constraint_type_sk": {
                "table": "dim_jao_constraint_type",
                "dimension_key": "dim_jao_constraint_type_sk",
                "value_column": "jao_constraint_type"
            },

            "dim_value_unit_sk": {
                "table": "dim_value_unit",
                "dimension_key": "dim_value_unit_sk",
                "value_column": "value_unit"
            }
        },

        "series_keys": [
            "datetime_begin",
            "dim_granularity_sk",
            "dim_data_provider_sk",
            "dim_jao_power_grid_sk",
            "dim_jao_constraint_type_sk",
            "dim_value_unit_sk"
        ],

        "insert_columns": [
            "datetime_begin",
            "dim_granularity_sk",
            "dim_data_provider_sk",
            "dim_jao_power_grid_sk",
            "dim_jao_constraint_type_sk",
            "fact_value",
            "dim_value_unit_sk"
        ]
    },
    # ========================================================
    # INTRADAY
    # ========================================================

    "fact_intraday": {

        "fact_table": "fact_intraday",

        "dimensions": {

            "dim_granularity_sk": {
                "table": "dim_granularity",
                "dimension_key": "dim_granularity_sk",
                "value_column": "granularity"
            },

            "dim_data_provider_sk": {
                "table": "dim_data_provider",
                "dimension_key": "dim_data_provider_sk",
                "value_column": "data_provider"
            },

            "dim_country_sk": {
                "table": "dim_country",
                "dimension_key": "dim_country_sk",
                "value_column": "country_name"
            },

            "dim_power_grid_sk": {
                "table": "dim_power_grid",
                "dimension_key": "dim_power_grid_sk",
                "value_column": "power_grid"
            },

            "dim_intraday_type_sk": {
                "table": "dim_intraday_type",
                "dimension_key": "dim_intraday_type_sk",
                "value_column": "intraday_type"
            },

            "dim_value_type_sk": {
                "table": "dim_value_type",
                "dimension_key": "dim_value_type_sk",
                "value_column": "value_type"
            },

            "dim_value_unit_sk": {
                "table": "dim_value_unit",
                "dimension_key": "dim_value_unit_sk",
                "value_column": "value_unit"
            }
        },

        "series_keys": [
            "datetime_begin",
            "dim_granularity_sk",
            "dim_data_provider_sk",
            "dim_country_sk",
            "dim_power_grid_sk",
            "dim_intraday_type_sk",
            "dim_value_type_sk",
            "dim_value_unit_sk"
        ],

        "insert_columns": [
            "datetime_begin",
            "dim_granularity_sk",
            "dim_data_provider_sk",
            "dim_country_sk",
            "dim_power_grid_sk",
            "dim_intraday_type_sk",
            "dim_value_type_sk",
            "fact_value",
            "dim_value_unit_sk"
        ]
    },


    # ========================================================
    # AUCTION FORECAST
    # ========================================================

    "fact_auction_forecast": {

        "fact_table": "fact_auction_forecast",

        "dimensions": {

            "dim_granularity_sk": {
                "table": "dim_granularity",
                "dimension_key": "dim_granularity_sk",
                "value_column": "granularity"
            },

            "dim_data_provider_sk": {
                "table": "dim_data_provider",
                "dimension_key": "dim_data_provider_sk",
                "value_column": "data_provider"
            },

            "dim_forecast_provider_sk": {
                "table": "dim_forecast_provider",
                "dimension_key": "dim_forecast_provider_sk",
                "value_column": "forecast_provider"
            },

            "dim_country_sk": {
                "table": "dim_country",
                "dimension_key": "dim_country_sk",
                "value_column": "country_name"
            },

            "dim_power_grid_sk": {
                "table": "dim_power_grid",
                "dimension_key": "dim_power_grid_sk",
                "value_column": "power_grid"
            },

            "dim_forecast_type_sk": {
                "table": "dim_forecast_type",
                "dimension_key": "dim_forecast_type_sk",
                "value_column": "forecast_type"
            },

            "dim_auction_type_sk": {
                "table": "dim_auction_type",
                "dimension_key": "dim_auction_type_sk",
                "value_column": "auction_type"
            },

            "dim_value_type_sk": {
                "table": "dim_value_type",
                "dimension_key": "dim_value_type_sk",
                "value_column": "value_type"
            },

            "dim_value_unit_sk": {
                "table": "dim_value_unit",
                "dimension_key": "dim_value_unit_sk",
                "value_column": "value_unit"
            }
        },

        "series_keys": [
            "datetime_begin",
            "dim_granularity_sk",
            "dim_data_provider_sk",
            "dim_forecast_provider_sk",
            "dim_country_sk",
            "dim_power_grid_sk",
            "dim_forecast_type_sk",
            "dim_auction_type_sk",
            "dim_value_type_sk",
            "dim_value_unit_sk"
        ],

        "insert_columns": [
            "datetime_begin",
            "forecast_datetime",
            "dim_granularity_sk",
            "dim_data_provider_sk",
            "dim_forecast_provider_sk",
            "dim_country_sk",
            "dim_power_grid_sk",
            "dim_forecast_type_sk",
            "dim_auction_type_sk",
            "dim_value_type_sk",
            "fact_value",
            "dim_value_unit_sk"
        ]
    },


    # ========================================================
    # PRODUCTION FORECAST
    # ========================================================

    "fact_production_forecast": {

        "fact_table": "fact_production_forecast",

        "dimensions": {

            "dim_granularity_sk": {
                "table": "dim_granularity",
                "dimension_key": "dim_granularity_sk",
                "value_column": "granularity"
            },

            "dim_data_provider_sk": {
                "table": "dim_data_provider",
                "dimension_key": "dim_data_provider_sk",
                "value_column": "data_provider"
            },

            "dim_forecast_provider_sk": {
                "table": "dim_forecast_provider",
                "dimension_key": "dim_forecast_provider_sk",
                "value_column": "forecast_provider"
            },

            "dim_country_sk": {
                "table": "dim_country",
                "dimension_key": "dim_country_sk",
                "value_column": "country_name"
            },

            "dim_power_grid_sk": {
                "table": "dim_power_grid",
                "dimension_key": "dim_power_grid_sk",
                "value_column": "power_grid"
            },

            "dim_production_type_sk": {
                "table": "dim_production_type",
                "dimension_key": "dim_production_type_sk",
                "value_column": "production_type"
            },

            "dim_forecast_type_sk": {
                "table": "dim_forecast_type",
                "dimension_key": "dim_forecast_type_sk",
                "value_column": "forecast_type"
            },

            "dim_value_type_sk": {
                "table": "dim_value_type",
                "dimension_key": "dim_value_type_sk",
                "value_column": "value_type"
            },

            "dim_value_unit_sk": {
                "table": "dim_value_unit",
                "dimension_key": "dim_value_unit_sk",
                "value_column": "value_unit"
            }
        },

        "series_keys": [
            "datetime_begin",
            "dim_granularity_sk",
            "dim_data_provider_sk",
            "dim_forecast_provider_sk",
            "dim_country_sk",
            "dim_power_grid_sk",
            "dim_production_type_sk",
            "dim_forecast_type_sk",
            "dim_value_type_sk",
            "dim_value_unit_sk"
        ],

        "insert_columns": [
            "datetime_begin",
            "forecast_datetime",
            "dim_granularity_sk",
            "dim_data_provider_sk",
            "dim_forecast_provider_sk",
            "dim_country_sk",
            "dim_power_grid_sk",
            "dim_production_type_sk",
            "dim_forecast_type_sk",
            "dim_value_type_sk",
            "fact_value",
            "dim_value_unit_sk"
        ]
    },


    # ========================================================
    # CONSUMPTION FORECAST
    # ========================================================

    "fact_consumption_forecast": {

        "fact_table": "fact_consumption_forecast",

        "dimensions": {

            "dim_granularity_sk": {
                "table": "dim_granularity",
                "dimension_key": "dim_granularity_sk",
                "value_column": "granularity"
            },

            "dim_data_provider_sk": {
                "table": "dim_data_provider",
                "dimension_key": "dim_data_provider_sk",
                "value_column": "data_provider"
            },

            "dim_forecast_provider_sk": {
                "table": "dim_forecast_provider",
                "dimension_key": "dim_forecast_provider_sk",
                "value_column": "forecast_provider"
            },

            "dim_country_sk": {
                "table": "dim_country",
                "dimension_key": "dim_country_sk",
                "value_column": "country_name"
            },

            "dim_power_grid_sk": {
                "table": "dim_power_grid",
                "dimension_key": "dim_power_grid_sk",
                "value_column": "power_grid"
            },

            "dim_consumption_type_sk": {
                "table": "dim_consumption_type",
                "dimension_key": "dim_consumption_type_sk",
                "value_column": "consumption_type"
            },

            "dim_forecast_type_sk": {
                "table": "dim_forecast_type",
                "dimension_key": "dim_forecast_type_sk",
                "value_column": "forecast_type"
            },

            "dim_value_type_sk": {
                "table": "dim_value_type",
                "dimension_key": "dim_value_type_sk",
                "value_column": "value_type"
            },

            "dim_value_unit_sk": {
                "table": "dim_value_unit",
                "dimension_key": "dim_value_unit_sk",
                "value_column": "value_unit"
            }
        },

        "series_keys": [
            "datetime_begin",
            "dim_granularity_sk",
            "dim_data_provider_sk",
            "dim_forecast_provider_sk",
            "dim_country_sk",
            "dim_power_grid_sk",
            "dim_consumption_type_sk",
            "dim_forecast_type_sk",
            "dim_value_type_sk",
            "dim_value_unit_sk"
        ],

        "insert_columns": [
            "datetime_begin",
            "forecast_datetime",
            "dim_granularity_sk",
            "dim_data_provider_sk",
            "dim_forecast_provider_sk",
            "dim_country_sk",
            "dim_power_grid_sk",
            "dim_consumption_type_sk",
            "dim_forecast_type_sk",
            "dim_value_type_sk",
            "fact_value",
            "dim_value_unit_sk"
        ]
    },

    # ========================================================
    # AUCTION
    # ========================================================

    "fact_auction": {

        "fact_table": "fact_auction",

        "dimensions": {

            "dim_granularity_sk": {
                "table": "dim_granularity",
                "dimension_key": "dim_granularity_sk",
                "value_column": "granularity"
            },

            "dim_data_provider_sk": {
                "table": "dim_data_provider",
                "dimension_key": "dim_data_provider_sk",
                "value_column": "data_provider"
            },

            "dim_power_grid_sk": {
                "table": "dim_power_grid",
                "dimension_key": "dim_power_grid_sk",
                "value_column": "power_grid"
            },

            "dim_auction_type_sk": {
                "table": "dim_auction_type",
                "dimension_key": "dim_auction_type_sk",
                "value_column": "auction_type"
            },

            "dim_value_unit_sk": {
                "table": "dim_value_unit",
                "dimension_key": "dim_value_unit_sk",
                "value_column": "value_unit"
            }
        },

        "series_keys": [
            "datetime_begin",
            "dim_granularity_sk",
            "dim_data_provider_sk",
            "dim_power_grid_sk",
            "dim_auction_type_sk",
            "dim_value_unit_sk"
        ],

        "insert_columns": [
            "datetime_begin",
            "dim_granularity_sk",
            "dim_data_provider_sk",
            "dim_power_grid_sk",
            "dim_auction_type_sk",
            "fact_value",
            "dim_value_unit_sk"
        ]
    },

    # ========================================================
    # COUNTER TRADING
    # ========================================================

    "fact_counter_trading": {

        "fact_table": "fact_counter_trading",

        "dimensions": {

            "dim_granularity_sk": {
                "table": "dim_granularity",
                "dimension_key": "dim_granularity_sk",
                "value_column": "granularity"
            },

            "dim_data_provider_sk": {
                "table": "dim_data_provider",
                "dimension_key": "dim_data_provider_sk",
                "value_column": "data_provider"
            },

            "dim_power_grid_sk": {
                "table": "dim_power_grid",
                "dimension_key": "dim_power_grid_sk",
                "value_column": "power_grid"
            },

            "dim_value_type_sk": {
                "table": "dim_value_type",
                "dimension_key": "dim_value_type_sk",
                "value_column": "value_type"
            },

            "dim_countertrading_type_sk": {
                "table": "dim_countertrading_type",
                "dimension_key": "dim_countertrading_type_sk",
                "value_column": "countertrading_type"
            },

            "dim_value_unit_sk": {
                "table": "dim_value_unit",
                "dimension_key": "dim_value_unit_sk",
                "value_column": "value_unit"
            }
        },

        "series_keys": [
            "datetime_begin",
            "dim_granularity_sk",
            "dim_data_provider_sk",
            "dim_power_grid_sk",
            "dim_value_type_sk",
            "dim_countertrading_type_sk",
            "dim_value_unit_sk"
        ],

        "insert_columns": [
            "datetime_begin",
            "dim_granularity_sk",
            "dim_data_provider_sk",
            "dim_power_grid_sk",
            "dim_value_type_sk",
            "dim_countertrading_type_sk",
            "fact_value",
            "dim_value_unit_sk"
        ]
    },


    # ========================================================
    # POWER FLOW FORECAST
    # ========================================================

    "fact_power_flow_forecast": {

        "fact_table": "fact_power_flow_forecast",

        "dimensions": {

            "dim_granularity_sk": {
                "table": "dim_granularity",
                "dimension_key": "dim_granularity_sk",
                "value_column": "granularity"
            },

            "dim_data_provider_sk": {
                "table": "dim_data_provider",
                "dimension_key": "dim_data_provider_sk",
                "value_column": "data_provider"
            },

            "dim_forecast_provider_sk": {
                "table": "dim_forecast_provider",
                "dimension_key": "dim_forecast_provider_sk",
                "value_column": "forecast_provider"
            },

            "dim_country_sk": {
                "table": "dim_country",
                "dimension_key": "dim_country_sk",
                "value_column": "country_name"
            },

            "dim_power_grid_from_sk": {
                "table": "dim_power_grid",
                "dimension_key": "dim_power_grid_sk",
                "value_column": "power_grid"
            },

            "dim_power_grid_to_sk": {
                "table": "dim_power_grid",
                "dimension_key": "dim_power_grid_sk",
                "value_column": "power_grid"
            },

            "dim_power_flow_type_sk": {
                "table": "dim_power_flow_type",
                "dimension_key": "dim_power_flow_type_sk",
                "value_column": "power_flow_type"
            },

            "dim_forecast_type_sk": {
                "table": "dim_forecast_type",
                "dimension_key": "dim_forecast_type_sk",
                "value_column": "forecast_type"
            },

            "dim_value_type_sk": {
                "table": "dim_value_type",
                "dimension_key": "dim_value_type_sk",
                "value_column": "value_type"
            },

            "dim_value_unit_sk": {
                "table": "dim_value_unit",
                "dimension_key": "dim_value_unit_sk",
                "value_column": "value_unit"
            }
        },

        "series_keys": [
            "datetime_begin",
            "dim_granularity_sk",
            "dim_data_provider_sk",
            "dim_forecast_provider_sk",
            "dim_country_sk",
            "dim_power_grid_from_sk",
            "dim_power_grid_to_sk",
            "dim_power_flow_type_sk",
            "dim_forecast_type_sk",
            "dim_value_type_sk",
            "dim_value_unit_sk"
        ],

        "insert_columns": [
            "datetime_begin",
            "forecast_datetime",
            "dim_granularity_sk",
            "dim_data_provider_sk",
            "dim_forecast_provider_sk",
            "dim_country_sk",
            "dim_power_grid_from_sk",
            "dim_power_grid_to_sk",
            "dim_power_flow_type_sk",
            "dim_forecast_type_sk",
            "dim_value_type_sk",
            "fact_value",
            "dim_value_unit_sk"
        ]
    }
}


# ============================================================
# CREATE DATABASE ENGINE
# ============================================================

def create_db_engine():

    password = PASSWORD

    if not password:
        raise ValueError(
            "RDS_PASSWORD environment variable is not set"
        )

    url = URL.create(
        drivername="postgresql+psycopg2",
        username=DB_USER,
        password=password,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME
    )

    return create_engine(url)

def insert(
    data: pd.DataFrame,
    table: str
):

    # --------------------------------------------------------
    # 1. Validate table
    # --------------------------------------------------------

    if table not in FORECAST_CONFIG:
        raise ValueError(
            f"table must be one of: "
            f"{list(FORECAST_CONFIG.keys())}"
        )

    config = FORECAST_CONFIG[table]

    fact_table = config["fact_table"]
    dimension_config = config["dimensions"]
    series_keys = config["series_keys"]
    insert_columns = config["insert_columns"]

    # --------------------------------------------------------
    # 2. Check whether table has forecast_datetime
    # --------------------------------------------------------

    has_forecast_datetime = (
        "forecast_datetime" in insert_columns
    )

    # --------------------------------------------------------
    # 3. Validate dataframe columns
    # --------------------------------------------------------

    missing_columns = (
        set(insert_columns)
        - set(data.columns)
    )

    if missing_columns:

        raise ValueError(
            f"Missing dataframe columns for {table}: "
            f"{sorted(missing_columns)}"
        )

    # --------------------------------------------------------
    # 4. Create DB connection
    # --------------------------------------------------------

    engine = create_db_engine()

    try:

        data = data.copy()

        print()
        print("=" * 60)
        print(f"{table.upper()} LOAD")
        print("=" * 60)

        # ====================================================
        # DIMENSION MAPPING
        # ====================================================

        print()
        print("Dimension mapping")
        print("-----------------")

        missing_any = False

        # ----------------------------------------------------
        # 5. Map dimensions -> surrogate keys
        # ----------------------------------------------------

        for fact_dim_column, dim_config in dimension_config.items():

            dim_table = dim_config["table"]
            dimension_key = dim_config["dimension_key"]
            value_column = dim_config["value_column"]

            original_values = (
                data[fact_dim_column]
                .copy()
            )

            dim_data = pd.read_sql(
                text(
                    f"""
                    SELECT
                        {dimension_key},
                        {value_column}
                    FROM public.{dim_table}
                    """
                ),
                engine
            )

            mapping = (
                dim_data
                .set_index(value_column)[dimension_key]
            )

            data[fact_dim_column] = (
                data[fact_dim_column]
                .map(mapping)
            )

            missing_mask = (
                data[fact_dim_column]
                .isna()
            )

            if missing_mask.any():

                missing_any = True

                missing_values = (
                    original_values
                    .loc[missing_mask]
                    .drop_duplicates()
                    .tolist()
                )

                print()
                print(
                    f"FAILED: {fact_dim_column}"
                )
                print(
                    f"Dimension table: {dim_table}"
                )
                print(
                    f"Affected rows: "
                    f"{missing_mask.sum():,}"
                )
                print(
                    f"Missing values: "
                    f"{missing_values}"
                )

            else:

                print(
                    f"OK: {fact_dim_column}"
                )

        # ----------------------------------------------------
        # 6. Stop if dimension mapping failed
        # ----------------------------------------------------

        if missing_any:

            raise ValueError(
                "One or more dimension values "
                "could not be mapped"
            )

        # ----------------------------------------------------
        # 7. Convert dimension columns to integers
        # ----------------------------------------------------

        dimension_columns = list(
            dimension_config.keys()
        )

        data[dimension_columns] = (
            data[dimension_columns]
            .astype("int64")
        )

        # ====================================================
        # DATETIME
        # ====================================================

        # ----------------------------------------------------
        # 8. datetime_begin always exists
        # ----------------------------------------------------

        data["datetime_begin"] = (
            pd.to_datetime(
                data["datetime_begin"],
                utc=True
            )
            .dt.tz_convert(None)
        )

        # ----------------------------------------------------
        # 9. forecast_datetime only for forecast tables
        # ----------------------------------------------------

        if has_forecast_datetime:

            data["forecast_datetime"] = (
                pd.to_datetime(
                    data["forecast_datetime"],
                    utc=True
                )
                .dt.tz_convert(None)
            )

        # ====================================================
        # LOAD EXISTING DATA
        # ====================================================

        key_sql = ",\n".join(
            series_keys
        )

        # ----------------------------------------------------
        # 10. Forecast table
        # ----------------------------------------------------

        if has_forecast_datetime:

            latest_sql = f"""
                SELECT DISTINCT ON (
                    {key_sql}
                )
                    {key_sql},
                    fact_value AS previous_fact_value

                FROM public.{fact_table}

                ORDER BY
                    {key_sql},
                    forecast_datetime DESC
            """

        # ----------------------------------------------------
        # 11. Non-forecast table, e.g. fact_intraday
        # ----------------------------------------------------

        else:

            latest_sql = f"""
                SELECT
                    {key_sql},
                    fact_value AS previous_fact_value

                FROM public.{fact_table}
            """

        latest = pd.read_sql(
            text(latest_sql),
            engine
        )

        # ----------------------------------------------------
        # 12. Normalize database datetime
        # ----------------------------------------------------

        latest["datetime_begin"] = (
            pd.to_datetime(
                latest["datetime_begin"],
                utc=True
            )
            .dt.tz_convert(None)
        )

        # ====================================================
        # COMPARE DATA
        # ====================================================

        data = data.merge(
            latest,
            on=series_keys,
            how="left"
        )

        rows_received = len(data)

        changed_mask = (
            data["previous_fact_value"].isna()
            |
            (
                data["fact_value"]
                != data["previous_fact_value"]
            )
        )

        rows_unchanged = int(
            (~changed_mask).sum()
        )

        data_to_insert = (
            data.loc[changed_mask]
            .copy()
        )

        rows_to_insert = len(
            data_to_insert
        )

        print()
        print("Data comparison")
        print("---------------")

        print(
            f"Rows received:          "
            f"{rows_received:,}"
        )

        print(
            f"Rows unchanged/skipped: "
            f"{rows_unchanged:,}"
        )

        print(
            f"Rows changed/new:       "
            f"{rows_to_insert:,}"
        )

        # ----------------------------------------------------
        # 13. Stop if nothing changed
        # ----------------------------------------------------

        if data_to_insert.empty:

            print()
            print(
                "No new or changed rows "
                "to insert."
            )

            with engine.connect() as connection:

                total_rows = connection.execute(
                    text(
                        f"""
                        SELECT COUNT(*)
                        FROM public.{fact_table}
                        """
                    )
                ).scalar_one()

            print(
                f"Total rows in table: "
                f"{total_rows:,}"
            )

            return

        # ====================================================
        # BULK INSERT
        # ====================================================

        values = list(
            data_to_insert[
                insert_columns
            ].itertuples(
                index=False,
                name=None
            )
        )

        insert_column_sql = ",\n".join(
            insert_columns
        )

        insert_sql = f"""
            INSERT INTO public.{fact_table} (
                {insert_column_sql}
            )

            VALUES %s

            ON CONFLICT DO NOTHING

            RETURNING 1;
        """

        raw_conn = engine.raw_connection()

        try:

            with raw_conn.cursor() as cur:

                inserted_rows = execute_values(
                    cur,
                    insert_sql,
                    values,
                    page_size=5000,
                    fetch=True
                )

            raw_conn.commit()

        except Exception as e:

            raw_conn.rollback()

            print()
            print("DATABASE INSERT FAILED")
            print("----------------------")
            print(
                f"Error type: "
                f"{type(e).__name__}"
            )
            print(
                f"Error message: {e}"
            )

            raise

        finally:

            raw_conn.close()

        # ====================================================
        # RESULTS
        # ====================================================

        actual_inserted = len(
            inserted_rows
        )

        conflicts = (
            rows_to_insert
            - actual_inserted
        )

        with engine.connect() as connection:

            total_rows = connection.execute(
                text(
                    f"""
                    SELECT COUNT(*)
                    FROM public.{fact_table}
                    """
                )
            ).scalar_one()

        print()
        print("Database insert result")
        print("----------------------")

        print(
            f"Rows received:          "
            f"{rows_received:,}"
        )

        print(
            f"Rows unchanged/skipped: "
            f"{rows_unchanged:,}"
        )

        print(
            f"Rows sent to database:  "
            f"{rows_to_insert:,}"
        )

        print(
            f"Actually inserted:      "
            f"{actual_inserted:,}"
        )

        print(
            f"Conflicts skipped:      "
            f"{conflicts:,}"
        )

        print(
            f"Total rows in table:    "
            f"{total_rows:,}"
        )

        if conflicts > 0:

            print()
            print("WARNING")
            print("-------")

            print(
                f"{conflicts:,} rows were skipped "
                f"because they conflicted with "
                f"the UNIQUE constraint."
            )

    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as e:

        print()
        print("LOAD FAILED")
        print("-----------")

        print(
            f"Table: {table}"
        )

        print(
            f"Error type: "
            f"{type(e).__name__}"
        )

        print(
            f"Error message: {e}"
        )

        raise

    finally:

        engine.dispose()


def get_data(sql: str) -> pd.DataFrame:

    engine = create_db_engine()

    try:

        data = pd.read_sql(
            text(sql),
            engine
        )

        return data

    except Exception as e:

        print("DATABASE QUERY FAILED")
        print("---------------------")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {e}")

        raise

    finally:

        engine.dispose()


