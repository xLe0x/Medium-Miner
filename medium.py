from functions import (
    searchGoogle,
    AuthorMedium,
)
from external import bcolors
import argparse

try:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-w",
        "--word",
        help="Search by word in google example: python3 medium.py -w xss",
    )
    parser.add_argument(
        "-a",
        "--author",
        help="Search by author in medium example: python3 medium.py -a ammarmosaber",
    )
    args = parser.parse_args()

    if args.word:
        searchGoogle(str(args.word))

    if args.author:
        AuthorMedium(str(args.author))

except ValueError:
    print(f"{bcolors.FAIL}Username is wrong or there is no blogs!{bcolors.ENDC}")
# except:
#     print(f"{bcolors.FAIL}Something went wrong please try again!{bcolors.ENDC}")
