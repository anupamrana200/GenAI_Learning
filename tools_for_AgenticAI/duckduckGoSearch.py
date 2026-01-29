#DuckDuckGo can give very current news.
from langchain_community.tools import DuckDuckGoSearchRun

search_tool = DuckDuckGoSearchRun()

result = search_tool.invoke("Today, most hot news about india.")

print(result)