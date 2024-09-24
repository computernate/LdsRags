import requests
from bs4 import BeautifulSoup
import pymysql


# Function to get HTML content
def get_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def parse_html_early(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Extracting year
    year_tag = soup.find('div', id='talklabel').find('a')
    year = year_tag.text.split('–')[0].strip()

    title_tag = soup.find('p', class_='gctitle')
    title = title_tag.text.strip()

    # Extracting author
    author_tag = soup.find('p', class_='gcspeaker')
    author = author_tag.text.replace('By ', '').strip()

    # Extracting role
    role_tag = soup.find('p', class_='gcspkpos')

    if not role_tag:
        role = 'None'
    else:
         role = role_tag.text.strip()

    content_tags = soup.find('div', class_='gcbody').find_all('p')

    content = []
    for tag in content_tags:
        for sup in tag.find_all('span'):
            sup.decompose()
        content.append(tag.get_text(separator=' ', strip=True))
    content = "\n".join(content)


    return year, title, author, role, content


def parse_html_mid(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Extracting year
    year_tag = soup.find('div', id='talklabel').find('a')
    year = year_tag.text.split('–')[0].strip()

    title_tag = soup.find('h1')
    title = title_tag.text.strip()

    author_div = soup.find('h2', class_='author')
    if not author_div:
        author_div =  soup.find('section', class_='author')
    author_div = author_div.find('div', class_='byline')
    author = author_div.find_all('p')[0].text.strip()
    if len(author_div.find_all('p')) > 1:
        role = author_div.find_all('p')[1].text.strip()
    else:
        role = "None"
    content_tags = soup.find('div', id='primary').find_all('p')

    content = []
    for tag in content_tags:
        for sup in tag.find_all('span'):
            sup.decompose()
        content.append(tag.get_text(separator=' ', strip=True))
    content = "\n".join(content)


    return year, title, author, role, content


# Function to parse HTML and extract data
def parse_html_late(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Extracting year
    year_tag = soup.find('div', id='talklabel').find('a')
    year = year_tag.text.split('–')[0].strip()

    # Extracting author
    author_tag = soup.find('p', class_='author-name')
    if author_tag:
        author = author_tag.text.strip()
    else:
        author = "None"

    # Extracting role
    role_tag = soup.find('p', class_='author-role')
    if role_tag:
        role = role_tag.text.strip()
    else:
        role = "None"

    # Extracting title
    title_tag = soup.find('h1', id='title1')
    if title_tag:
        title = title_tag.text.strip()
    else:
        title = "None"

    # Extracting content and removing <sup> tags
    content_tags = soup.find('div', class_='body-block').find_all('p')

    content = []
    for tag in content_tags:
        for sup in tag.find_all('sup'):
            sup.decompose()
        content.append(tag.get_text(separator=' ', strip=True))
    content = "\n".join(content)

    return year, title, author, role, content


# Function to save data to the database
def save_to_db(year, title, author, role, content):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='3nT3R#mysql',
        database='LDSRags',
        port=3307
    )

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO ConferenceTalks (content, role, author, year, title) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (content, role, author, year, title))
        connection.commit()
    finally:
        connection.close()


# Main script
if __name__ == "__main__":
    for i in range(8617 , 8734):
        url = f"https://scriptures.byu.edu/content/talks_ajax/{i}"
        try:
            html = get_html(url)
        except Exception as e:
            print(f"Talk {i} does not exist")
            continue

        try:
            year, title, author, role, content = parse_html_late(html)
        except AttributeError as e:
            try:
                year, title, author, role, content = parse_html_early(html)
            except AttributeError as e:
                year, title, author, role, content = parse_html_mid(html)
        save_to_db(year, title, author, role, content)
        print(f"Data {i} saved successfully")