import requests, markdownify, os, xmltodict
from re import match
from googlesearch import search
from external import bcolors


def save_MD_files(data, i):
    print(f"{bcolors.OKCYAN}Started to download {i}!{bcolors.ENDC}")
    try:
        with open(
            f'{i} - {data["channel"]["item"][int(i)]["title"]}.md',
            "x",
        ) as mdfile:
            mdfile.write(
                markdownify.markdownify(
                    dict(data["channel"]["item"][int(i)]).get("content:encoded")
                    or dict(data["channel"]["item"][int(i)]).get("description")
                )
            )

    except FileExistsError:
        print(f"#{i} file is already downloaded")


def download_MD_files(data, user_choice, isNumber, isComma, isAll):
    if isComma:
        if user_choice.split(",")[-1] == "":
            print("you suck")
        elif "," in user_choice:
            for i in user_choice.split(","):
                save_MD_files(data, user_choice)

    if isNumber:
        save_MD_files(data, user_choice)

    if isAll:
        for i, _ in enumerate(data["channel"]["item"]):
            save_MD_files(data, int(i))


def getResults(rss_url):
    response = requests.get(rss_url)
    if response.status_code != 200:
        raise ValueError()

    rss_data = xmltodict.parse(response.content)
    json_data = {}
    json_data["channel"] = {}
    for key, value in rss_data["rss"]["channel"].items():
        json_data["channel"][key] = value

    json_data["items"] = []
    for item in rss_data["rss"]["channel"]["item"]:
        json_item = {}
        for key, value in item.items():
            json_item[key] = value
        json_data["items"].append(json_item)

    return json_data


def listBlogs(data):
    if data:
        print()
        print("Here is a list of all the blogs:")
        for i, item in enumerate(data["channel"]["item"]):
            if not dict(item).get("content:encoded"):
                print(
                    f"{bcolors.BOLD}{i} - {item['title']}{bcolors.WARNING} (Member-Only Story){bcolors.ENDC}{bcolors.ENDC}"
                )
            else:
                print(f"{bcolors.BOLD}{i} - {item['title']}{bcolors.ENDC}")

    else:
        raise ValueError()


def checkUserInput(data):
    print()
    user_choice = input(
        f"{bcolors.OKGREEN}(A number,numbers (comma separated) or 'all' to downlaod): {bcolors.ENDC}"
    )
    print()
    if user_choice.isnumeric():
        download_MD_files(data, user_choice, isNumber=True, isAll=False, isComma=False)
    elif "," in user_choice:
        download_MD_files(data, user_choice, isComma=True, isNumber=False, isAll=False)
    elif user_choice == "all":
        download_MD_files(data, user_choice, isAll=True, isComma=False, isNumber=False)
    else:
        raise Exception()


def checkForDir(author):
    if getResults(f"https://medium.com/@{author}/feed"):
        if not os.path.exists(f"{author}_blogs"):
            os.mkdir(f"{author}_blogs")

        os.chdir(f"{author}_blogs")


def searchGoogle(userInput):
    def extractUsername(url):
        try:
            return match(r"https:\/\/(.*)\/@(.*)/", url).group(2)
        except:
            return Exception()

    query = f"site:medium.com {userInput}"

    for result in search(query, num=20, stop=25, pause=1):
        if "@" in result:
            print()
            print(f"{bcolors.BOLD}The Author: {extractUsername(result)} {bcolors.ENDC}")
            print(f"{bcolors.OKGREEN}{result} {bcolors.ENDC}")


def AuthorMedium(author):
    data = getResults(f"https://medium.com/@{author}/feed")
    listBlogs(data)
    checkForDir(author)
    checkUserInput(data)
