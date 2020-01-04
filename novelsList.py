from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

def fetchNovelsList(page):
    def fetchImage(novel):
        return novel.find("div", {"class": "search_img_nu"}).img["src"]
        
    def fetchTitle(novel):
        return novel.find("div", {"class": "search_title"}).a.text

    def fetchChapters(novel):
        return novel.find("div", {"class": "search_stats"}).find_all("span")[0].text.strip().split()[0]

    def fetchFrequency(novel):
        return novel.find("div", {"class": "search_stats"}).find_all("span")[1].text.strip().split()[1]

    def fetchReviews(novel):
        return novel.find("div", {"class": "search_stats"}).find_all("span")[3].text.strip().split()[0]

    def fetchRating(novel):
        return novel.find("div", {"class": "search_ratings"}).text

    def fetchLastUpdated(novel):
        return novel.find("div", {"class": "search_stats"}).find_all("span")[4].text.strip()

    def fetchCompleted(novel):
        completed = False
        if (novel.find("a", {"class": "gennew complete"})):
            completed = True
        return completed

    def fetchGenres(novel, genres_html):
        genres = []

        for genre_html in genres_html:
            genres.append(genre_html.text)
        
        return genres

    def fetchDescription(novel, genres_html):
        body_text = novel.find("div", {"class": "search_body_nu"}).text
        last_genre = genres_html[len(genres_html) - 1].text
        last_genre_index = body_text.find(last_genre)

        return body_text[last_genre_index + len(last_genre):].replace("... more>>", "").replace(" <<less", "")
        
    my_url = "https://www.novelupdates.com/novelslisting/?sort=7&order=1&status=1&pg={0}".format(page)
    req = Request(my_url, headers={'User-Agent': 'Mozilla/5.0'})

    client = urlopen(req)
    html = client.read()
    client.close()

    page_soup = soup(html, "html.parser")
    novels = page_soup.find_all("div", {"class": "search_main_box_nu"})

    novels_data = []

    for novel in novels:
        image = fetchImage(novel)
        title = fetchTitle(novel)
        chapters = fetchChapters(novel)
        frequency = fetchFrequency(novel)
        reviews = fetchReviews(novel)
        rating = fetchRating(novel)
        last_updated = fetchLastUpdated(novel)
        completed = fetchCompleted(novel)

        genres_html = novel.find_all("a", {"class": "gennew search"})

        genres = fetchGenres(novel, genres_html)
        description = fetchDescription(novel, genres_html)

        novel_data = {
            "image": image,
            "title": title,
            "chapters": chapters,
            "frequency": frequency,
            "reviews": reviews,
            "rating": rating,
            "last_updated": last_updated,
            "completed": completed,
            "genres": genres,
            "description": description
        }
        novels_data.append(novel_data)

    print(novels_data)
    return novels_data