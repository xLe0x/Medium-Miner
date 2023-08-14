from functions import (
    searchGoogle,
    SearchAuthorMedium,
)
from external import bcolors
import argparse,sys


parser = argparse.ArgumentParser(description="Medium Miner.")

word_group = parser.add_mutually_exclusive_group()
word_group.add_argument(
    "-w",
    "--word",
    type=str,
    help="Search by word in google example: python3 medium.py -w xss",
)

parser.add_argument(
    "-c",
    "--count",
    type=int,
    help="How many output you want? example: python3 medium.py -w idor -c 10",
)

parser.add_argument(
    "-a",
    "--author",
    type=str,
    help="Search by author in medium example: python3 medium.py -a ammarmosaber",
)

parser.add_argument("-v", action="store_true", help="Prints the program version")

args = parser.parse_args()


try:
    if args.word:
        if not args.count:
            args.count = 10
        searchGoogle(str(args.word), args.count)

    elif args.author:
        SearchAuthorMedium(args.author)

    elif args.v:
        print("1.0 Beta")

    else:
        print()
        parser.print_help()
        print()

except ValueError:
    print(f"{bcolors.FAIL}Username is wrong or there is no blogs!{bcolors.ENDC}")
except:
    print(f"{bcolors.FAIL}Something went wrong please try again!{bcolors.ENDC}")
