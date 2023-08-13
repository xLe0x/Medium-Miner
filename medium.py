from functions import getResults,listBlogs,checkUserInput,checkForDir
from external import bcolors




author = input(
    f"{bcolors.BOLD}Enter The author name https://medium.com/feed/@NAME_HERE: {bcolors.ENDC}"
)

try:
    data = getResults(author)

    listBlogs(data)

    checkForDir(author)

    checkUserInput(data)
    
except NameError:
    print(f"{bcolors.FAIL}Username is wrong or there is no blogs!{bcolors.ENDC}")
except:
    print(f"{bcolors.FAIL}Something went wrong please try again!{bcolors.ENDC}")
