import requests
import pandas as pd

from playwright.sync_api import sync_playwright

import src.inserter as inserter


# ============================================================
# SETTINGS
# ============================================================

DAY_AHEAD_API_URL = (
    "https://dataportal-api.nordpoolgroup.com/"
    "api/DayAheadPrices"
)


IDA2_PAGE_URL = (
    "https://data.nordpoolgroup.com/"
    "auction/intraday-auction-2/prices"
)


DELIVERY_AREA = "DK1"
CURRENCY = "EUR"


# ============================================================
# FINAL FACT_AUCTION COLUMNS
# ============================================================

FACT_AUCTION_COLUMNS = [
    "datetime_begin",
    "dim_granularity_sk",
    "dim_data_provider_sk",
    "dim_power_grid_sk",
    "dim_auction_type_sk",
    "fact_value",
    "dim_value_unit_sk",
]


# ============================================================
# CLEAN FINAL AUCTION DATA
# ============================================================

def clean_auction_data(
    data: pd.DataFrame,
) -> pd.DataFrame:

    if data.empty:

        return pd.DataFrame(
            columns=FACT_AUCTION_COLUMNS
        )


    data = data.copy()


    # ========================================================
    # DATETIME
    # ========================================================

    data[
        "datetime_begin"
    ] = pd.to_datetime(
        data[
            "datetime_begin"
        ],
        utc=True,
        errors="coerce",
    )


    # ========================================================
    # FACT VALUE
    # ========================================================

    data[
        "fact_value"
    ] = pd.to_numeric(
        data[
            "fact_value"
        ],
        errors="coerce",
    )


    # ========================================================
    # REMOVE INVALID
    # ========================================================

    data = data.dropna(
        subset=[
            "datetime_begin",
            "fact_value",
        ]
    )


    # ========================================================
    # KEEP REQUIRED COLUMNS
    # ========================================================

    data = data[
        FACT_AUCTION_COLUMNS
    ]


    # ========================================================
    # REMOVE DUPLICATES FROM SAME DOWNLOAD
    # ========================================================

    data = (
        data
        .drop_duplicates(
            subset=FACT_AUCTION_COLUMNS
        )
        .sort_values(
            "datetime_begin"
        )
        .reset_index(
            drop=True
        )
    )


    return data


# ============================================================
# IDA1
# DOWNLOAD ONE DELIVERY DATE
# ============================================================

def get_ida1_for_date(
    date: str,
    delivery_area: str = DELIVERY_AREA,
    currency: str = CURRENCY,
) -> tuple[pd.DataFrame, bool]:

    try:

        print()
        print("=" * 70)
        print("NORD POOL IDA1")
        print("=" * 70)

        print(
            f"Date: "
            f"{date}"
        )

        print(
            f"Area: "
            f"{delivery_area}"
        )


        # ====================================================
        # REQUEST PARAMETERS
        # ====================================================

        params = {
            "date":
                date,

            "market":
                "SIDC_IntradayAuction1",

            "deliveryArea":
                delivery_area,

            "currency":
                currency,
        }


        # ====================================================
        # REQUEST
        # ====================================================

        response = requests.get(
            DAY_AHEAD_API_URL,
            params=params,
            timeout=60,
        )


        print(
            f"Status: "
            f"{response.status_code}"
        )


        # ====================================================
        # NO CONTENT
        # ====================================================

        if response.status_code == 204:

            print(
                "No IDA1 data available."
            )

            return (
                pd.DataFrame(),
                True,
            )


        response.raise_for_status()


        payload = response.json()


        # ====================================================
        # ENTRIES
        # ====================================================

        entries = payload.get(
            "multiAreaEntries",
            [],
        )


        if not entries:

            print(
                "No IDA1 entries returned."
            )

            return (
                pd.DataFrame(),
                True,
            )


        rows = []


        # ====================================================
        # LOOP DELIVERY PERIODS
        # ====================================================

        for entry in entries:

            delivery_start = entry.get(
                "deliveryStart"
            )


            entry_per_area = entry.get(
                "entryPerArea",
                {},
            )


            fact_value = entry_per_area.get(
                delivery_area
            )


            if (
                delivery_start is None
                or
                fact_value is None
            ):

                continue


            rows.append(
                {
                    "datetime_begin":
                        delivery_start,

                    "dim_granularity_sk":
                        "15_MIN",

                    "dim_data_provider_sk":
                        "NORDPOOL",

                    "dim_power_grid_sk":
                        delivery_area,

                    "dim_auction_type_sk":
                        "IDA1",

                    "fact_value":
                        fact_value,

                    "dim_value_unit_sk":
                        "EUR/MWH",
                }
            )


        data = pd.DataFrame(
            rows
        )


        data = clean_auction_data(
            data
        )


        print()
        print(
            f"IDA1 rows: "
            f"{len(data):,}"
        )


        return (
            data,
            True,
        )


    except Exception as error:

        print()
        print(
            "IDA1 DOWNLOAD FAILED"
        )
        print(
            "--------------------"
        )

        print(
            f"Error type: "
            f"{type(error).__name__}"
        )

        print(
            f"Error message: "
            f"{error}"
        )


        return (
            pd.DataFrame(),
            False,
        )


# ============================================================
# IDA1
# DOWNLOAD X DAYS BACK THROUGH TOMORROW
# ============================================================

def get_ida1(
    days_back: int = 1,
) -> tuple[pd.DataFrame, bool]:

    try:

        if not isinstance(
            days_back,
            int,
        ):

            raise TypeError(
                "days_back must be an integer"
            )


        if days_back < 0:

            raise ValueError(
                "days_back cannot be negative"
            )


        today = (
            pd.Timestamp.now(
                tz="Europe/Copenhagen"
            )
            .normalize()
        )


        start_date = (
            today
            - pd.Timedelta(
                days=days_back
            )
        )


        end_date = (
            today
            + pd.Timedelta(
                days=1
            )
        )


        dates = pd.date_range(
            start=start_date,
            end=end_date,
            freq="D",
        )


        frames = []


        print()
        print("=" * 70)
        print("DOWNLOADING IDA1")
        print("=" * 70)

        print(
            f"From: "
            f"{start_date.date()}"
        )

        print(
            f"To:   "
            f"{end_date.date()}"
        )


        for date in dates:

            date_string = date.strftime(
                "%Y-%m-%d"
            )


            data_day, ok = (
                get_ida1_for_date(
                    date=date_string,
                    delivery_area=DELIVERY_AREA,
                    currency=CURRENCY,
                )
            )


            if not ok:

                print(
                    f"IDA1 failed for "
                    f"{date_string}"
                )

                continue


            if data_day.empty:

                continue


            frames.append(
                data_day
            )


        if not frames:

            print(
                "No IDA1 data returned."
            )

            return (
                pd.DataFrame(),
                False,
            )


        data = pd.concat(
            frames,
            ignore_index=True,
        )


        data = clean_auction_data(
            data
        )


        return (
            data,
            True,
        )


    except Exception as error:

        print()
        print(
            "IDA1 DOWNLOAD FAILED"
        )

        print(
            f"Error type: "
            f"{type(error).__name__}"
        )

        print(
            f"Error message: "
            f"{error}"
        )


        return (
            pd.DataFrame(),
            False,
        )


# ============================================================
# IDA2
# RESPONSE HANDLER
# ============================================================

def handle_ida2_response(
    response,
    captured_json: list,
) -> None:

    try:

        content_type = (
            response.headers
            .get(
                "content-type",
                "",
            )
            .lower()
        )


        if (
            "application/json"
            not in content_type
        ):

            return


        payload = response.json()


        captured_json.append(
            payload
        )


    except Exception:

        pass


# ============================================================
# FIND IDA2 ROWS INSIDE JSON
# ============================================================

def extract_ida2_rows(
    payload,
    delivery_area: str,
) -> list:

    rows = []


    # ========================================================
    # LIST
    # ========================================================

    if isinstance(
        payload,
        list,
    ):

        for item in payload:

            rows.extend(
                extract_ida2_rows(
                    payload=item,
                    delivery_area=delivery_area,
                )
            )


        return rows


    # ========================================================
    # NOT DICT
    # ========================================================

    if not isinstance(
        payload,
        dict,
    ):

        return rows


    # ========================================================
    # TRY TO READ THIS OBJECT AS A PRICE ROW
    # ========================================================

    delivery_start = (
        payload.get(
            "deliveryStart"
        )
        or
        payload.get(
            "startTime"
        )
        or
        payload.get(
            "start"
        )
    )


    fact_value = None


    # ========================================================
    # AREA DICTIONARIES
    # ========================================================

    for key in [
        "entryPerArea",
        "prices",
        "values",
    ]:

        area_values = payload.get(
            key
        )


        if isinstance(
            area_values,
            dict,
        ):

            if (
                delivery_area
                in area_values
            ):

                fact_value = area_values[
                    delivery_area
                ]

                break


    # ========================================================
    # DIRECT PRICE VALUE
    # ========================================================

    if fact_value is None:

        for key in [
            "price",
            "auctionPrice",
            "value",
        ]:

            if key in payload:

                fact_value = payload[
                    key
                ]

                break


    # ========================================================
    # SAVE ROW
    # ========================================================

    if (
        delivery_start is not None
        and
        fact_value is not None
    ):

        try:

            fact_value = float(
                fact_value
            )


            rows.append(
                {
                    "datetime_begin":
                        delivery_start,

                    "dim_granularity_sk":
                        "15_MIN",

                    "dim_data_provider_sk":
                        "NORDPOOL",

                    "dim_power_grid_sk":
                        delivery_area,

                    "dim_auction_type_sk":
                        "IDA2",

                    "fact_value":
                        fact_value,

                    "dim_value_unit_sk":
                        "EUR/MWH",
                }
            )


        except (
            TypeError,
            ValueError,
        ):

            pass


    # ========================================================
    # RECURSIVELY SEARCH CHILD OBJECTS
    # ========================================================

    for value in payload.values():

        if isinstance(
            value,
            (
                dict,
                list,
            ),
        ):

            rows.extend(
                extract_ida2_rows(
                    payload=value,
                    delivery_area=delivery_area,
                )
            )


    return rows


# ============================================================
# IDA2
# DOWNLOAD PAGE
# ============================================================

def get_ida2_prices(
    delivery_date: str = "latest",
    delivery_area: str = DELIVERY_AREA,
    currency: str = CURRENCY,
) -> tuple[pd.DataFrame, bool]:

    try:

        print()
        print("=" * 70)
        print("NORD POOL IDA2")
        print("=" * 70)

        print(
            f"Delivery date: "
            f"{delivery_date}"
        )

        print(
            f"Area: "
            f"{delivery_area}"
        )


        # ====================================================
        # URL
        # ====================================================

        url = (
            f"{IDA2_PAGE_URL}"
            f"?deliveryDate={delivery_date}"
            f"&currency={currency}"
            f"&aggregation=DeliveryPeriod"
            f"&deliveryAreas={delivery_area}"
        )


        captured_json = []


        # ====================================================
        # PLAYWRIGHT
        # ====================================================

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True
            )


            context = browser.new_context(
                locale="en-GB"
            )


            page = context.new_page()


            # =================================================
            # RESPONSE CALLBACK
            # =================================================

            response_handler = (
                lambda response:
                handle_ida2_response(
                    response=response,
                    captured_json=captured_json,
                )
            )


            page.on(
                "response",
                response_handler,
            )


            # =================================================
            # OPEN PAGE
            # =================================================

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=120_000,
            )


            # Give API calls time to complete
            page.wait_for_timeout(
                8000
            )


            # =================================================
            # REMOVE LISTENER
            # =================================================

            try:

                page.remove_listener(
                    "response",
                    response_handler,
                )

            except Exception:

                pass


            browser.close()


        # ====================================================
        # CHECK CAPTURED RESPONSES
        # ====================================================

        print(
            f"Captured JSON responses: "
            f"{len(captured_json):,}"
        )


        if not captured_json:

            print(
                "No IDA2 JSON responses captured."
            )

            return (
                pd.DataFrame(),
                False,
            )


        # ====================================================
        # EXTRACT PRICE ROWS
        # ====================================================

        rows = []


        for payload in captured_json:

            rows.extend(
                extract_ida2_rows(
                    payload=payload,
                    delivery_area=delivery_area,
                )
            )


        # ====================================================
        # DATAFRAME
        # ====================================================

        data = pd.DataFrame(
            rows
        )


        if data.empty:

            print(
                "No usable IDA2 prices found."
            )

            return (
                pd.DataFrame(),
                False,
            )


        data = clean_auction_data(
            data
        )


        print()
        print(
            f"IDA2 rows: "
            f"{len(data):,}"
        )

        print(
            f"First delivery: "
            f"{data['datetime_begin'].min()}"
        )

        print(
            f"Last delivery:  "
            f"{data['datetime_begin'].max()}"
        )


        return (
            data,
            True,
        )


    except Exception as error:

        print()
        print(
            "IDA2 DOWNLOAD FAILED"
        )
        print(
            "--------------------"
        )

        print(
            f"Error type: "
            f"{type(error).__name__}"
        )

        print(
            f"Error message: "
            f"{error}"
        )


        return (
            pd.DataFrame(),
            False,
        )



# ============================================================
# INSERT IDA1
# ============================================================

def insert_ida1(
    days_back: int = 1,
) -> bool:

    try:

        data, ok = get_ida1(
            days_back=days_back
        )

        if not ok:

            print(
                "IDA1 download failed."
            )

            return False


        if data.empty:

            print(
                "No IDA1 data returned."
            )

            return True


        inserter.insert(
            data,
            table="fact_auction",
        )


        print()
        print(
            f"Inserted "
            f"{len(data):,} "
            f"IDA1 rows into "
            f"fact_auction."
        )


        return True


    except Exception as error:

        print()
        print(
            "IDA1 INSERT FAILED"
        )
        print(
            "------------------"
        )

        print(
            f"Error type: "
            f"{type(error).__name__}"
        )

        print(
            f"Error message: "
            f"{error}"
        )


        return False


# ============================================================
# INSERT IDA2
# ============================================================

def insert_ida2(
    delivery_date: str = "latest",
) -> bool:

    try:

        data, ok = get_ida2_prices(
            delivery_date=delivery_date,
            delivery_area=DELIVERY_AREA,
            currency=CURRENCY,
        )


        if not ok:

            print(
                "IDA2 download failed."
            )

            return False


        if data.empty:

            print(
                "No IDA2 data returned."
            )

            return True


        inserter.insert(
            data,
            table="fact_auction",
        )


        print()
        print(
            f"Inserted "
            f"{len(data):,} "
            f"IDA2 rows into "
            f"fact_auction."
        )


        return True


    except Exception as error:

        print()
        print(
            "IDA2 INSERT FAILED"
        )
        print(
            "------------------"
        )

        print(
            f"Error type: "
            f"{type(error).__name__}"
        )

        print(
            f"Error message: "
            f"{error}"
        )


        return False