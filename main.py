import argparse

from src.download_ida_auctions import (
    insert_ida1,
    insert_ida2,
)


# ============================================================
# CURRENT IDA1
# ============================================================

def run_ida1_current() -> bool:

    print()
    print("=" * 70)
    print(
        "RUNNING CURRENT IDA1 INSERT"
    )
    print("=" * 70)


    return insert_ida1(
        days_back=1
    )




# ============================================================
# CURRENT IDA2
# ============================================================

def run_ida2_current() -> bool:

    print()
    print("=" * 70)
    print(
        "RUNNING CURRENT IDA2 INSERT"
    )
    print("=" * 70)


    return insert_ida2(
        delivery_date="latest"
    )


# ============================================================
# MAIN
# ============================================================

def main(
    argv=None,
) -> int:

    parser = argparse.ArgumentParser(
        description=(
            "Run Nord Pool IDA1 "
            "or IDA2 inserts."
        )
    )


    parser.add_argument(
        "--job",
        required=True,
        choices=[
            "ida1_current",
            "ida2_current",
        ],
        help=(
            "ida1_current = IDA1 1 day back, "
            "ida2_current = latest IDA2"
        ),
    )


    args = parser.parse_args(
        argv
    )


    # ========================================================
    # IDA1 CURRENT
    # ========================================================

    if args.job == "ida1_current":

        ok = run_ida1_current()




    # ========================================================
    # IDA2 CURRENT
    # ========================================================

    elif args.job == "ida2_current":

        ok = run_ida2_current()


    else:

        print(
            f"Unsupported job: "
            f"{args.job}"
        )

        return 1


    print()
    print(
        f"main :: ok is {ok}"
    )


    return (
        0
        if ok
        else 1
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    raise SystemExit(
        main()
    )

# if __name__ == "__main__":
#
#     raise SystemExit(
#         main(
#             [
#                 "--job",
#                 "ida2_current",
#             ]
#         )
#     )