from instagram import WebAgentAccount, Account, Location, Tag, WebAgent
from instagram.exceptions import AuthException
from urllib.parse import quote
import db
import time


class InstaParser:
    def __init__(self):
        self.agent = None
        self.min_folowers = 0
        self.data_location_count = 0
        self.window = None
        self.locations_file = 'locations.csv'
        self.tags_file = 'tags.csv'
        self.parsed_data = []

    def auth(self, login, password):
        try:
            self.agent = WebAgentAccount(login)
            self.agent.auth(password)
        except AuthException as ex:
            self.agent = None
            print(ex)

    def find_locations(self, location):
        url = f'https://www.instagram.com/web/search/topsearch/?context=blended&query={quote(location)}&rank_token=0.043242&include_reel=true'
        print(url)
        resp = self.agent.get_request(url)
        json_resp = resp.json()
        places = json_resp['places']
        print(places)
        places_dict = {}
        for place in places:
            places_dict[place['place']['location']['name']] = place['place']['location']['pk']
        return places_dict

    def find_tags(self, tag):
        url = f'https://www.instagram.com/web/search/topsearch/?context=blended&query={quote(tag)}&rank_token=0.84235424&include_reel=true'
        print(url)
        resp = self.agent.get_request(url)
        json_resp = resp.json()
        hashtags = json_resp['hashtags']
        print(hashtags)
        hashtags_dict = {}
        for hashtag in hashtags:
            hashtags_dict[hashtag['hashtag']['name']] = hashtag['hashtag']['id']
        return hashtags_dict

    def get_media_info(self, media):
        anonym_agent = WebAgent()
        try:
            anonym_agent.get_comments(media)
        except Exception as ex:
            return
        account_name = media.owner
        account = Account(media.owner)
        time.sleep(0.5)
        self.agent.get_followers(account=account, count=1, delay=1)
        # print(account.biography)
        # print(account.entry_data_path)
        followers = account.followers_count
        if int(followers) < self.min_folowers:
            return
        return account_name, followers

    # есть повторяющиеся части, разбить на методы
    def get_data_locations(self, index):
        location = Location(index)
        db.create_file(self.locations_file)
        medias, pointer = self.agent.get_media(location, count=10, delay=1)
        for media in medias:
            data = self.get_media_info(media)
            print(data)
            if not data:
                continue
            db.add_data(self.locations_file, data)
            self.data_location_count += 1
            if self.window:
                self.window.label_6.setText('Добавлено аккаунтов ' + str(self.data_location_count))
        while pointer:
            medias, pointer = self.agent.get_media(location, pointer=pointer, count=10, delay=1)
            for media in medias:
                data = self.get_media_info(media)
                print(data)
                if not data:
                    continue
                db.add_data(self.locations_file, data)
                self.data_location_count += 1
                if self.window:
                    self.window.label_6.setText('Добавлено аккаунтов ' + str(self.data_location_count))

    def get_data_tags(self, tag):
        tag = Tag(tag)
        print(tag.base_url)
        db.create_file(self.tags_file)
        medias, pointer = self.agent.get_media(tag, count=100, delay=1)
        for media in medias:
            data = self.get_media_info(media)
            print(data)
            if not data:
                continue
            if data in self.parsed_data:
                continue
            db.add_data(self.tags_file, data)
            self.data_location_count += 1
            self.parsed_data.append(data)
            if self.window:
                self.window.label_18.setText('Добавлено аккаунтов ' + str(self.data_location_count))
        while pointer:
            medias, pointer = self.agent.get_media(tag, pointer=pointer, count=100, delay=1)
            for media in medias:
                data = self.get_media_info(media)
                print(data)
                if not data:
                    continue
                if data in self.parsed_data:
                    continue
                db.add_data(self.locations_file, data)
                self.data_location_count += 1
                self.parsed_data.append(data)
                if self.window:
                    self.window.label_18.setText('Добавлено аккаунтов ' + str(self.data_location_count))


if __name__ == '__main__':
    parser = InstaParser()
    parser.auth('bears_bobruisk', 'a31081993abc')
    tags = parser.get_data_tags('москва')


