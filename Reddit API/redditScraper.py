import praw
import requests
from bs4 import BeautifulSoup

# Reddit API credentials
reddit = praw.Reddit(client_id='DSGa-45une1d4OFZaxrZ3g',
                     client_secret='zwtFHYAknNP6_laQurorW4k7M2jBcw',
                     user_agent='EddoBot/0.1 by EddoSellsCannons')

# Subreddit to scrape
subreddit_name = "BestAliExpressFinds"
subreddit = reddit.subreddit(subreddit_name)

# Function to search AliExpress
def search_aliexpress(query):
    url = f"https://www.aliexpress.com/wholesale?SearchText={query}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('div', class_='list-item')
        return items
    else:
        print("Error searching AliExpress:", response.status_code)
        print(response.content)  # Print HTML content for debugging
        return None

# Function to search eBay
def search_ebay(query):
    url = f"https://www.ebay.com/sch/i.html?_nkw={query}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('div', class_='s-item')
        return items
    else:
        print("Error searching eBay:", response.status_code)
        print(response.content)  # Print HTML content for debugging
        return None

check_limit = 1

# Iterate over top posts of the week
for submission in subreddit.top('week', limit=check_limit):
    if submission.score > 5:  # Check if the submission has more than 5 upvotes
        print(f"Title: {submission.title}")
        print(f"URL: {submission.url}")
        print(f"Score: {submission.score}")
        print(f"Number of comments: {submission.num_comments}")
        
        # Extract post price and title
        title_split = submission.title.split("]")
        if len(title_split) == 2:
            post_price = title_split[0][1:].strip()  # Remove square brackets and whitespace
            post_title = title_split[1][1:].strip()  # Remove whitespace
            
            # Search on AliExpress
            aliexpress_results = search_aliexpress(post_title)
            if aliexpress_results:
                aliexpress_price = aliexpress_results[0].find('span', class_='value').text.strip()
                print(f"AliExpress Price: {aliexpress_price}")
            else:
                print("No AliExpress results found")
            
            # Search on eBay
            ebay_results = search_ebay(post_title)
            if ebay_results:
                ebay_price = ebay_results[0].find('span', class_='s-item__price').text.strip()
                print(f"eBay Price: {ebay_price}")
            else:
                print("No eBay results found")
        
        # Wait until all comments are loaded
        submission.comments.replace_more(limit=None)
        
        # Find OP's comment with a link
        op_comment = None
        for comment in submission.comments:
            if comment.author == submission.author and 'http' in comment.body:
                op_comment = comment
                break
        
        if op_comment:
            print(f"OP's comment: {op_comment.body}")

        print("\n")
