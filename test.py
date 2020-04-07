import time
from instagram import WebAgentAccount, Account, Location, Media, WebAgent

COUNTRYS = {
    'united states': 389983831
}
agent = WebAgentAccount("domimod1")
agent.auth("a31081993")
url = 'https://www.instagram.com/web/search/topsearch/?context=blended&query=Mins&rank_token=0&include_reel=true'
find_request = agent.get_request(url).json()
places = find_request['places']
for place in places:
    print(place['place']['location']['name'])
# prof = Account('macmiller')
# time.sleep(1)
# anonym_agent = WebAgent()
# #followers = agent.get_followers(account=prof, count=10, delay=2)
# medias, pointer = agent.get_media(Location(COUNTRYS['united states']), delay=1, count=10)
# for media in medias:
#     try:
#         comments = anonym_agent.get_comments(media)
#     except Exception as ex:
#         continue
#     print(media.owner)
# while pointer:
#     medias, pointer = agent.get_media(Location(COUNTRYS['united states']), pointer=pointer, delay=1, count=10)
#     for media in medias:
#         try:
#             comments = anonym_agent.get_comments(media)
#         except Exception as ex:
#             continue
#         print(media.owner)