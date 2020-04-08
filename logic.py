from instagram import WebAgentAccount, Account, Location, Media, WebAgent
from instagram.exceptions import AuthException
from urllib.parse import quote


class InstaParser:
    def __init__(self):
        self.agent = None
        self.min_folowers_locations = 0
        self.data_location_count = 0
        self.window = None

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

    def get_media_info(self, media):
        anonym_agent = WebAgent()
        try:
            anonym_agent.get_comments(media)
        except Exception as ex:
            return
        account_name = media.owner
        account = Account(media.owner)
        self.agent.get_followers(account=Account(media.owner), count=1, delay=1)
        followers = account.followers_count
        if int(followers) < self.min_folowers_locations:
            return
        return account_name, followers

    def get_data(self, index):
        medias, pointer = self.agent.get_media(Location(index), count=10, delay=1)
        for media in medias:
            data = self.get_media_info(media)
            print(data)
            if not data:
                continue
            self.data_location_count += 1
            if self.window:
                self.window.label_6.setText('Добавлено аккаунтов ' + str(self.data_location_count))
        while pointer:
            medias, pointer = self.agent.get_media(Location(index), pointer=pointer, count=10, delay=1)
            for media in medias:
                data = self.get_media_info(media)
                if not data:
                    continue
                self.data_location_count += 1
                if self.window:
                    self.window.label_6.setText('Добавлено аккаунтов ' + str(self.data_location_count))

if __name__ == '__main__':
    parser = InstaParser()
    parser.auth('domimod1', 'a31081993')
    parser.find_locations('Москва')
