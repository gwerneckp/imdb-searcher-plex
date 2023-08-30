import requests
import argparse
import re
from bs4 import BeautifulSoup


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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
        title = title_element['content'].split(' ⭐')[0]

        # Find the IMDb ID
        imdb_id_match = re.search(r'/title/(tt\d+)/', url)
        imdb_id = imdb_id_match.group(1) if imdb_id_match else None

        if title and imdb_id:
            formatted_result = f"{title} {{imdb-{imdb_id}}}"
            return formatted_result
        else:
            return "Error: Unable to extract title and IMDb ID."

    except requests.exceptions.RequestException as e:
        return f"Error: {e}"


def main():
    parser = argparse.ArgumentParser(
        description='Scrape and format IMDb title and ID.')
    parser.add_argument('movie_name', nargs='*', help='Name of the movie')
    parser.add_argument('--url', '-u', type=str, help='IMDb URL of the title')
    args = parser.parse_args()

    if args.movie_name:
        search_query = ' '.join(args.movie_name)
        search_results = search_movie_by_name(search_query)
        if search_results:
            max_name_length = 0
            for result in search_results:
                if result.get('l') and result.get('y') and result.get('id'):
                    formatted_name = f"{result['l']} ({result['y']}) {{imdb-{result['id']}}}"
                    if len(formatted_name) > max_name_length:
                        max_name_length = len(formatted_name)

                    result['formatted'] = formatted_name

            for result in search_results:
                print(
                    f"{result.get('formatted'):<{max_name_length}}{bcolors.OKBLUE} || {result.get('s')} {bcolors.ENDC}")

        else:
            print("No search results found.")
    elif args.url:
        formatted_result = scrape_and_format(args.url)
        print(formatted_result)
    else:
        print("Please provide a search query or an IMDb URL.")


if __name__ == '__main__':
    main()
