from aiow import Aiow

# Headers
__headers__ = {
    'Host': 'www.chosic.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'X-WP-Nonce': 'e30a8d4858',
    'app': 'playlist_generator',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'Referer': 'https://www.chosic.com/playlist-generator/',
    'Cookie': 'pll_language=en; FCNEC=%5B%5B%22AKsRol_W_zfppVTNZrCqi2CFbUka1gY8TQahdH3ZHIi76nzBysgha_loHfbeGdaPNz9k-34vJiqVdtO5WTjCRn5MaBcDsw2lnnK403nXRfaFot6zdInqWK-78-cmLSPUYYeSZK2aQj7ThpaGFyTCOC-LbRVJ-PNozQ%3D%3D%22%5D%5D',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'TE': 'trailers'
}


class Chos:
    """
    Get recommendation based on ['track', 'artist', 'playlist', 'genre']
    Search based on ['track', 'artist', 'playlist']
    Get Details based on ['track', 'artist', 'playlist']

    Usage:
       - Chos.Search('Powerwolf', basedon='artist', limit=10)
       - Chos.GetDetails('0bUgTRe5st6TMbRCEjKezX', basedon='track', limit=10)
       - Chos.GetRecommendation('0bUgTRe5st6TMbRCEjKezX', basedon='track', limit=10)
    """

    class OperationError(Exception):
        def __init__(self, error_text):
            self.error_text = error_text
            super().__init__(error_text)

    # Search By ['track', 'artist', 'playlist']
    @classmethod
    async def Search(cls, query: str, basedon: str, limit=30) -> dict:
        """
        Search based on ['track', 'artist', 'playlist']

        - query:str  Search query
        - basedon:str Based on track, artist or playlist
        - limit:int Range(1, 100)
        """
        params = {'q': query, 'type': basedon, 'limit': limit}
        url = 'https://www.chosic.com/api/tools/search'
        r = await Aiow.Get(url, headers=__headers__, params=params)
        print(r)
        if basedon == 'artist': return r['artists']['items']
        elif basedon == 'track': return r['tracks']['items']
        elif basedon == 'playlist': return r['playlists']['items']
        else: raise cls.OperationError("Invalid basedon, Available: ['tracks', 'artists', 'playlists']")

    # Get Details By ['track', 'artist', 'playlist']
    @classmethod
    async def GetDetails(cls, seedid: str, basedon: str) -> dict:
        """
        Get Details based on ['track', 'artist', 'playlist']

        - seedid:str Track/artist/playlist id
        - basedon:str Based on track, artist, playlist
        - limit:int Range(1, 100)
        """
        if basedon not in ['track', 'artist', 'playlist']: raise cls.OperationError("Invalid basedon, Available: ['tracks', 'artists', 'playlists']")
        url = f'https://www.chosic.com/api/tools/{basedon}s/{seedid}'
        r = await Aiow.Get(url, headers=__headers__)
        return r

    # Get Similar Songs By ['track', 'artist', 'playlist', 'genre']
    @classmethod
    async def GetRecommendation(cls, seedid: str, basedon: str, limit=30) -> dict:
        """
        Get recommendation based on ['track', 'artist', 'playlist', 'genre']

        - seedid:str Track/artist/playlist id or genre name
        - basedon:str Based on track, artist, playlist or genre
        - limit:int Range(1, 100)
        """
        if basedon == 'genre': params = {'based_on': 'genre', 'genre': seedid, 'limit': limit}
        elif basedon == 'playlist': params = {'based_on': 'playlist', 'playlist_id': seedid, 'limit': limit}
        elif basedon == 'track': params = {'seed_tracks': seedid, 'limit': limit}
        elif basedon == 'artist': params = {'seed_artists': seedid, 'limit': limit}
        else: raise cls.OperationError("Invalid basedon, Available: ['track', 'artist', 'playlist', 'genre']")

        url = 'https://www.chosic.com/api/tools/recommendations'
        r = await Aiow.Get(url, headers=__headers__, params=params)
        return r['tracks'] if 'tracks' in r.keys() else r
