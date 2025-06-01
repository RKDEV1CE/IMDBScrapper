import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
headers = {'User-Agent': UserAgent().random}

def get_imdb_cast_and_characters(movie_id):
    url = f"https://www.imdb.com/title/{movie_id}/fullcredits/"
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    cast_section = soup.find('div', {'data-testid': 'sub-section-cast'})
    if not cast_section:
        print("Cast section not found")
        return []
    cast_list = []
    cast_items = cast_section.find_all('li', {'data-testid': 'name-credits-list-item'})
    for item in cast_items:
        actor_tag = item.find('a', class_="name-credits--title-text-big")
        if not actor_tag:
            actor_tag = item.find('a', class_="name-credits--title-text-small")

        actor_name = actor_tag.text.strip() if actor_tag else None

        character_tag = item.find('a', href=True)
        character_name = None
        for a in item.find_all('a', href=True):
            if '/characters/' in a['href']:
                character_name = a.text.strip()
                break

        if actor_name:
            cast_list.append({
                'actor': actor_name,
                'character': character_name or 'N/A'
            })

    return cast_list

# Example usage
def get_cast(movie_id):
    #movie_id = "tt21191806"
    cast_data = get_imdb_cast_and_characters(movie_id)
    cast_list = []
    for person in cast_data:
        cast_list.append((person['actor'], person['character']))
    
    return cast_list
