from instagram import WebAgentAccount, Account, Location, Media, WebAgent
from instagram.exceptions import AuthException
from urllib.parse import unquote,quote

class InstaParser:
    def __init__(self):
        self.agent = None

    def auth(self, login, password):
        try:
            self.agent = WebAgentAccount(login)
            self.agent.auth(password)
        except AuthException as ex:
            self.agent = None
            print(ex)

    def find_locations(self, location):
        url = f'https://www.instagram.com/web/search/topsearch/?context=blended&query={quote(location)}&rank_token=0&include_reel=true'
        resp = self.agent.get_request(url)
        json_resp = resp.json()
        places = json_resp['places']
        places_dict = {}
        for place in places:
            places_dict[place['place']['location']['pk']] = place['place']['location']['name']
        return places_dict

if __name__ == '__main__':
    parser = InstaParser()
    parser.auth('domimod1', 'a31081993')
    parser.find_locations('Москва')
