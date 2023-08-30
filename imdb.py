import requests
import argparse
import re

def search_movie_by_name(movie_name):
    url = f"https://v3.sg.media-imdb.com/suggestion/titles/x/{movie_name.lower()}.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if 'd' in data:
            return data['d']
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None

def scrape_and_format(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the title
        title_element = soup.find('meta', property='og:title')
        title = title_element['content'].split(' - IMDb')[0]

        # Find the IMDb ID
        imdb_id_match = re.search(r'/title/(tt\d+)/', url)
        imdb_id = imdb_id_match.group(1) if imdb_id_match else None

        if title and imdb_id:
            formatted_result = f"{title} ({url.split('(')[-1].split(')')[0]}) {{imdb-{imdb_id}}}"
            return formatted_result
        else:
            return "Error: Unable to extract title and IMDb ID."

    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def main():
    parser = argparse.ArgumentParser(description='Scrape and format IMDb title and ID.')
    parser.add_argument('--url', '-u', type=str, help='IMDb URL of the title')
    parser.add_argument('--search', '-s', type=str, help='Search for a movie by name')
    args = parser.parse_args()

    if args.url:
        formatted_result = scrape_and_format(args.url)
        print(formatted_result)
    elif args.search:
        search_results = search_movie_by_name(args.search)
        if search_results:
            for result in search_results:
                if result.get('l') and result.get('y') and result.get('id'):
                    print(f"{result['l']} ({result['y']}) {{imdb-{result['id']}}}")
        else:
            print("No search results found.")
    else:
        print("Please provide either an IMDb URL or a search query.")

if __name__ == '__main__':
    main()
