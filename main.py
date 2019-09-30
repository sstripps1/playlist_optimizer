import sys
import spotipy
import spotipy.util as util
import pandas as pd

class PlaylistOptimizer(object):
    
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.token = self._authenticate_user()
    
    def _authenticate_user(self):
        scope = 'user-library-read'

        if len(sys.argv) > 1:
            username = sys.argv[1]
        else:
            print("Usage: %s username" % (sys.argv[0],))
            sys.exit()
        
        token = util.prompt_for_user_token(username, scope, client_id=self.client_id,
                                           client_secret=self.client_secret,
                                           redirect_uri=self.redirect_uri)
        
        return token
    
    def user_tracks(self):
        sp = spotipy.Spotify(auth=self.token)
        
        df = pd.DataFrame(columns=['Name','Artist','Album','Date Added','Duration','URI','Release Date','Popularity']).T
        offset = 0
        track_num = 1
        while True:
            limit = 50
            results = sp.current_user_saved_tracks(limit=limit, offset=offset)['items']

            for track in results:
                track_name = track['track']['name']
                artists = ','.join([artist['name'] for artist in track['track']['artists']])
                album = track['track']['album']['name']
                date_added = pd.to_datetime(track['added_at'])
                duration = track['track']['duration_ms']
                track_uri = track['track']['uri']
                release_date = pd.to_datetime(track['track']['album']['release_date']).date()
                popularity = track['track']['popularity']

                df[track_num] = [track_name, artists, album, date_added, duration, track_uri, release_date, popularity]
                track_num += 1

            offset += limit

            if len(results) < 50:
                break

        df = df.T
        
        return df
        
