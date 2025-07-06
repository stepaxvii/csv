from argparse import ArgumentParser

from tabulate import tabulate

from csv_processor import aggregate_rows, filter_rows, read_csv, sort_rows


def main():
    parser = ArgumentParser()
    parser.add_argument("--file", required=True,)
    parser.add_argument("--where")
    parser.add_argument("--order-by")
    parser.add_argument("--aggregate")
    args = parser.parse_args()
    rows = read_csv(args.file)

    if args.where:
        rows = filter_rows(rows, args.where)
    if args.order_by:
        if "=" in args.order_by:
            column, direction = args.order_by.split("=")
            reverse = direction.lower() == "desc"
        else:
            column = args.order_by
            reverse = False
        rows = sort_rows(rows, column, reverse)
    if args.aggregate:
        result = aggregate_rows(rows, args.aggregate)
        output = [
            [f"{args.aggregate}"],
            [f"{str(result)}"]
        ]
        print(tabulate(output, tablefmt="grid"))
    else:
        print(tabulate(rows, headers="keys", tablefmt="grid"))


if __name__ == "__main__":
    main()
