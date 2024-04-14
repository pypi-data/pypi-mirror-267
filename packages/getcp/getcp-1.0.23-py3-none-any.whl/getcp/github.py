from bs4 import BeautifulSoup
import requests

def get_github_stats(username):
    url = f'https://github.com/{username}?tab=repositories'
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        name_div = soup.find('h1', class_='vcard-names')
        name_tag = name_div.find('span', class_='p-name vcard-fullname d-block overflow-hidden')
        if name_tag:
            name = name_tag.text.strip()
        else:
            name = 'Not Specified'

        loc_li = soup.find('li', class_='vcard-detail pt-1 hide-sm hide-md')
        if loc_li:
            loc_tag = loc_li.find('span', class_='p-label')
            if loc_tag:
                loc = loc_tag.text.strip()
            else:
                loc = 'Not Specified'
        else:
            loc = 'Not Specified'

        repo_tags = soup.find_all('div', class_="col-10 col-lg-9 d-inline-block")
        repo_info = []
        for tag in repo_tags:
            repo_tag = tag.find('h3', class_= 'wb-break-all')
            repo_name = repo_tag.a.text.strip()
            lang = tag.find('span', itemprop="programmingLanguage")
            repo_link = repo_tag.a['href']
            if lang:
                lang = lang.text.strip()
            else:
                lang = "Not Specified"
            update_tag = tag.find('relative-time', class_='no-wrap')
            if update_tag:
                update = update_tag.text.strip()
            else:
                update = "Not Specified"
            repo_info.append({'repo_name': repo_name, 'link': repo_link ,'lang':lang, 'update': update})

        return {
            'name' : name,
            'location': loc,
            'repo_info': repo_info
        }

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
