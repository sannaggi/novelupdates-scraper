from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

# https://www.novelupdates.com/series/hackai-buster/

def fetchNovel(name):
    def response(name):
        my_url = "https://www.novelupdates.com/series/{}/".format(name)
        req = Request(my_url, headers={'User-Agent': 'Mozilla/5.0'})

        client = urlopen(req)
        html = client.read()
        client.close()

        page = soup(html, "html.parser")

        novel_data = {
            "image": fetchImage(page),
            "genres": fetchGenres(page),
            "description": fetchDescription(page),
            "type": fetchType(page),
            "tags": fetchTags(page),
            "votes": fetchVotes(page),
            "language": fetchLanguage(page),
            "authors": fetchAuthors(page),
            "artists": fetchArtists(page),
            "year": fetchYear(page),
            "status": fetchStatus(page)
        }

        return novel_data
    
    def fetchImage(page):
        return page.find("div", {"class": "seriesimg"}).img["src"]
    
    def fetchDescription(page):
        return page.find("div", {"id": "editdescription"}).p.text

    def fetchType(page):
        return page.find("a", {"class", "genre type"}).text
    
    def fetchGenres(page):
        genres = []
        genres_html = page.find("div", {"id": "seriesgenre"}).find_all("a")

        for genre_html in genres_html:
            genres.append(genre_html.text)

        return genres

    def fetchTags(page):
        tags = []
        tags_html = page.find("div", {"id": "showtags"}).find_all("a")

        for tag_html in tags_html:
            tags.append(tag_html.text)

        return tags

    def fetchVotes(page):
        votes = {}
        votes_html = page.find_all("span", {"class": "votetext"})
        score = 5

        for vote_html in votes_html:
            texts = vote_html.text.split()
            votes[score] = texts[1][1:]
            score -= 1
        
        return votes

    def fetchLanguage(page):
        return page.find("div", {"id": "showlang"}).a.text
    
    def fetchAuthors(page):
        authors = []
        authors_html = page.find("div", {"id": "showauthors"}).find_all("a")

        for author_html in authors_html:
            authors.append(author_html.text)
        
        return authors
    
    def fetchArtists(page):
        artists = []
        artists_html = page.find("div", {"id": "showartists"}).find_all("a")

        for artist_html in artists_html:
            artists.append(artist_html.text)
        
        return artists
    
    def fetchYear(page):
        return page.find("div", {"id": "edityear"}).text.strip()
    
    def fetchStatus(page):
        return page.find("div", {"id": "editstatus"}).text.strip()

    return response(name)