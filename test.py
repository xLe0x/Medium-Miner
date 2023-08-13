from functions import getResults, listBlogs, checkForDir, checkUserInput

data = getResults(f"https://medium.com/@ammarmosaber/feed")
listBlogs(data)
checkForDir("ammarmosaber")
checkUserInput(data)
