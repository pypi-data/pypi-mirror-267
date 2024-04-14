import requests
from bs4 import BeautifulSoup

def get_codeforces_stats(handle):
    base_url = f'https://codeforces.com/profile/{handle}'
    final_url = base_url

    try:
        response = requests.get(final_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        # codeforces_handle = soup.find('div', class_='info').find('span', class_='handle').text.strip()


        rating_section = soup.find('span', class_='user-gray', style='font-weight:bold;')
        rating = rating_section.text.strip() if rating_section else 'No rating'

        solved_problems_section = soup.find('div', class_='_UserActivityFrame_counterValue')
        solved_problems = int(solved_problems_section.text.split()[0]) if solved_problems_section else 0

        rank_section = soup.find('span', class_='user-gray')
        rank = rank_section.text.strip() if rank_section else 'No rank'

        return {
            # 'codeforces_handle': codeforces_handle,
            'rating': rating,
            'solved_problems': solved_problems,
            'rank': rank,
        }

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
