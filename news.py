import requests

def fetch_news():
    keyword = input("Enter a keyword to search news: ")
    api_key = "38b407279a88439aab83903b193f8580"  
    url = f"https://newsapi.org/v2/everything?q={keyword}&apiKey={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            news_data = response.json()
            for article in news_data['articles'][:5]:
                print(f"Title: {article['title']}, Source: {article['source']['name']}")
        else:
            print("Failed to fetch news. Please check your API key or network.")
    except requests.exceptions.RequestException:
        print("Network error. Please check your internet connection.")
