import re
from googlesearch import search
from external import bcolors


def extractUsername(url):
  """Extracts the username from the given URL."""

  return re.match(r"https:\/\/(.*)\/@(.*)/", url).group(2)



query = "site:medium.com xss"
authours = []
dskfjsdkf
for result in search(query, num=15, stop=15, pause=2):
    if "@" in result:
        result = extractUsername(result)
        results.append(result)

print(results)