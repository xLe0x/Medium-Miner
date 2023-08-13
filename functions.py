import requests,markdownify,os
from external import bcolors

def getResults(author):
     response =  requests.get(f"https://api.rss2json.com/v1/api.json?rss_url=https://medium.com/feed/@{author}")
     if response.ok:
        data =  response.json()
        return data


def listBlogs(data):
    if data != None:
        print()
        print("Here is a list of all the blogs:")
        for i, item in enumerate(data["items"]):
            if "Continue reading on Medium" not in item["content"]:
                print(f"{bcolors.BOLD}{i} - {item['title']}{bcolors.ENDC}")
            else:
                print(f"{bcolors.BOLD}{i} - {item['title']}{bcolors.WARNING} (Member-Only Story){bcolors.ENDC}{bcolors.ENDC}")
    else:
        raise NameError()



def checkUserInput(data):
        print()
        user_choice = input(
            f"{bcolors.OKGREEN}(A number,numbers (comma separated) or 'all' to downlaod): {bcolors.ENDC}"
        )
        print()
        if user_choice.isnumeric():
            try:
                with open(
                    f'{user_choice} - {data["items"][int(user_choice)]["title"]}.md', "x"
                ) as mdfile:
                    mdfile.write(
                        markdownify.markdownify(data["items"][int(user_choice)]["content"])
                    )
                print(f"{bcolors.OKCYAN}Started to download {user_choice}!{bcolors.ENDC}")
            except FileExistsError:
                print(f"{bcolors.FAIL}#{user_choice} file is already downloaded{bcolors.ENDC}")

        elif "," in user_choice:
            if user_choice.split(",")[-1] == "":
                print("you suck")
            else:
                for i in user_choice.split(","):
                    print(f"{bcolors.OKCYAN}Started to download {i}!{bcolors.ENDC}")
                    try:
                        with open(
                            f'{i} - {data["items"][int(i)]["title"]}.md',
                            "x",
                        ) as mdfile:
                            mdfile.write(
                                markdownify.markdownify(data["items"][int(i)]["content"])
                            )
                    except FileExistsError:
                        print(f"#{i} file is already downloaded")

        elif user_choice == "all":
            for i, item in enumerate(data["items"]):
                print(f"{bcolors.OKCYAN}Started to download {i}!{bcolors.ENDC}")
            try:
                with open(
                    f'{i} - {data["items"][int(i)]["title"]}.md',
                    "x",
                ) as mdfile:
                    mdfile.write(
                        markdownify.markdownify(data["items"][int(i)]["content"])
                    )
            except FileExistsError:
                print(f"{bcolors.FAIL}#{i} file is already downloaded{bcolors.ENDC}")

        else:
            raise Exception()


def checkForDir(author):
    if getResults(author) != None and checkUserInput(getResults(author)):
        if not os.path.exists(f"{author}_blogs"):
            os.mkdir(f"{author}_blogs")
            
        os.chdir(f"{author}_blogs")