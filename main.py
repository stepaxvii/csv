from argparse import ArgumentParser

from tabulate import tabulate

from csv_processor import aggregate_rows, filter_rows, read_csv


def main():
    parser = ArgumentParser()
    parser.add_argument("--file", required=True,)
    parser.add_argument("--where")
    parser.add_argument("--aggregate")
    args = parser.parse_args()
    rows = read_csv(args.file)

    if args.where:
        rows = filter_rows(rows, args.where)
    if args.aggregate:
        result = aggregate_rows(rows, args.aggregate)
        print(f"{args.aggregate} = {result}")
    else:
        print(tabulate(rows, headers="keys"))


if __name__ == "__main__":
    main()
