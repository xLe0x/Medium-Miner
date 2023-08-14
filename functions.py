import requests, markdownify, os
from re import match
from googlesearch import search
from external import bcolors
from bs4 import BeautifulSoup


def save_MD_files(blog, i):
    print(f"{bcolors.OKCYAN}Started to download {i}!{bcolors.ENDC}")
    try:
        with open(
            f'{i} - {blog[int(i)]["title"]}.md',
            "x",
        ) as mdfile:
            mdfile.write(markdownify.markdownify(blog[int(i)]["content"]))

    except FileExistsError:
        print(f"#{i} file is already downloaded")


def download_MD_files(blog, user_choice, isNumber, isComma, isAll):
    if isComma:
        if user_choice.split(",")[-1] == "":
            print("you suck")
        elif "," in user_choice:
            for i in user_choice.split(","):
                save_MD_files(blog, user_choice)

    if isNumber:
        save_MD_files(blog, user_choice)

    if isAll:
        for i, _ in enumerate(blog):
            save_MD_files(blog, int(i))


def getResults(url):
    blog_list = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features="xml")
    blogs = soup.findAll("item")
    for a in blogs:
        title = a.find("title").text
        link = a.find("link").text
        content = a.find("content:encoded")
        content = content.text if content is not None else ""
        blog = {"title": title, "link": link, "content": content}
        blog_list.append(blog)
    return blog_list


def listBlogs(blogs):
    if blogs:
        print()
        print("Here is a list of all the blogs:")
        for i, blog in enumerate(blogs):
            if blog["content"] == "":
                print(
                    f"{bcolors.BOLD}{i} - {blog['title']}{bcolors.WARNING} (Member-Only Story){bcolors.ENDC}{bcolors.ENDC}"
                )
            else:
                print(f"{bcolors.BOLD}{i} - {blog['title']}{bcolors.ENDC}")

    else:
        raise ValueError()


def checkUserInput(blogs):
    print()
    user_choice = input(
        f"{bcolors.OKGREEN}(A number,numbers (comma separated) or 'all' to downlaod): {bcolors.ENDC}"
    )
    print()
    if user_choice.isnumeric():
        download_MD_files(blogs, user_choice, isNumber=True, isAll=False, isComma=False)
    elif "," in user_choice:
        download_MD_files(blogs, user_choice, isComma=True, isNumber=False, isAll=False)
    elif user_choice == "all":
        download_MD_files(blogs, user_choice, isAll=True, isComma=False, isNumber=False)
    else:
        raise Exception()


def checkForDir(author):
    if getResults(f"https://medium.com/@{author}/feed"):
        if not os.path.exists(f"{author}_blogs"):
            os.mkdir(f"{author}_blogs")

        os.chdir(f"{author}_blogs")


def searchGoogle(userInput, count):
    def extractUsername(url):
        try:
            return match(r"https:\/\/(.*)\/@(.*)/", url).group(2)
        except:
            return Exception()

    query = f"site:medium.com {userInput}"

    for result in search(query, num=count, stop=count, pause=1):
        if "@" in result:
            print()
            print(f"{bcolors.BOLD}The Author: {extractUsername(result)} {bcolors.ENDC}")
            print(f"{bcolors.OKGREEN}{result} {bcolors.ENDC}")


def SearchAuthorMedium(author):
    data = getResults(f"https://medium.com/@{author}/feed")
    listBlogs(data)
    checkForDir(author)
    checkUserInput(data)
