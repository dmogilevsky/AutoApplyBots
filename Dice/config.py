username = ""
password = ""

# keywords to search by and blacklisted words in job title
keywords = ["developer", "software", "engineer", "c#", "python", "java", "sql", "golang"]
blacklist = ["architect", "principal", "manager", "product owner", "front end"]

wait_s = 5  # number of seconds for selenium to wait
cache_path = ""

# Create your desired search in dice, and paste the link here
SEARCH_URL_WITHOUT_PAGE = (f"https://www.dice.com/jobs?q=software engineer&countryCode=US&radius=30&radiusUnit=mi&page=%s&pageSize=100&filters.easyApply=true&filters.isRemote=true&language=en'")