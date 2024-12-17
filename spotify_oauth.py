import serial
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import speech_recognition as sr
from threading import Thread, Lock

# Speech Recognizer Setup
r = sr.Recognizer()
m = sr.Microphone()

# Spotify Authentication
client_id = ''
client_secret = ''
redirect_uri = 'http://localhost:5000/callback'

sp = spotipy.Spotify( auth_manager=SpotifyOAuth( client_id=client_id,
                                                 client_secret=client_secret,
                                                 redirect_uri=redirect_uri,
                                                 scope="user-modify-playback-state user-read-playback-state" ) )

ser = serial.Serial( 'COM3', 115200, timeout=0.05 )

# Global variables
last_volume = -1
last_volume_time = 0
MIN_UPDATE_INTERVAL = 0.2  # Minimum interval between updates in seconds
volume_lock = Lock()
exiting = False


# Function to adjust the volume
def set_volume( volume ):
    global last_volume, last_volume_time
    current_time = time.time()

    # Use lock to ensure thread safety
    with volume_lock:
        if current_time - last_volume_time < MIN_UPDATE_INTERVAL:
            return

        if abs( volume - last_volume ) >= 5:  # Only update if change is significant
            try:
                sp.volume( volume )
                print( f"Volume set to {volume}%" )
                last_volume = volume
                last_volume_time = current_time
            except spotipy.exceptions.SpotifyException as e:
                if e.http_status == 429:
                    print( "Rate limit exceeded. Pausing for 10 seconds..." )
                    time.sleep( 10 )
                else:
                    print( f"Spotify API error: {e}" )


def play_song( song_uri ):
    device_id = get_device_id()
    if not device_id:
        return

    try:
        sp.start_playback( device_id=device_id, uris=[ song_uri ] )
        print( "Playback started." )
    except Exception as e:
        handle_spotify_exception( e )


def play_playlist( playlist_uri ):
    device_id = get_device_id()
    if not device_id:
        return

    try:
        playlist_tracks = sp.playlist_tracks( playlist_uri )
        track_uris = [ track[ 'track' ][ 'uri' ] for track in playlist_tracks[ 'items' ] if track[ 'track' ] ]

        if not track_uris:
            print( "No tracks found in the playlist." )
            return

        sp.start_playback( device_id=device_id, uris=track_uris )
        print( "Playlist playback started." )
    except Exception as e:
        handle_spotify_exception( e )


def play_album( album_uri ):
    device_id = get_device_id()
    if not device_id:
        return

    try:
        album_tracks = sp.album_tracks( album_uri )
        track_uris = [ track[ 'uri' ] for track in album_tracks[ 'items' ] ]

        if not track_uris:
            print( "No tracks found in the album." )
            return

        sp.start_playback( device_id=device_id, uris=track_uris )
        print( "Album playback started." )
    except Exception as e:
        handle_spotify_exception( e )


def play_song_by_name( song_name ):
    song_name = song_name.strip()
    if not song_name:
        print( "Error: No song name provided." )
        return

    try:
        results = sp.search( q=song_name, type='track', limit=1 )
        if not results[ 'tracks' ][ 'items' ]:
            print( f"No song found for '{song_name}'." )
            return

        song_uri = results[ 'tracks' ][ 'items' ][ 0 ][ 'uri' ]
        song_name_result = results[ 'tracks' ][ 'items' ][ 0 ][ 'name' ]
        print( f"Playing '{song_name_result}'..." )
        play_song( song_uri )
    except Exception as e:
        handle_spotify_exception( e )


def play_album_by_name( album_name ):
    album_name = album_name.strip()
    if not album_name:
        print( "Error: No album name provided." )
        return

    try:
        results = sp.search( q=album_name, type='album', limit=1 )
        if not results[ 'albums' ][ 'items' ]:
            print( f"No album found for '{album_name}'." )
            return

        album_uri = results[ 'albums' ][ 'items' ][ 0 ][ 'uri' ]
        album_name_result = results[ 'albums' ][ 'items' ][ 0 ][ 'name' ]
        print( f"Playing album '{album_name_result}'..." )
        play_album( album_uri )
    except Exception as e:
        handle_spotify_exception( e )


def get_device_id( device_name="CRISTIANLAPTOP" ):
    devices = sp.devices()
    if not devices[ 'devices' ]:
        print( "No active devices found. Please open Spotify on your device." )
        return None

    for device in devices[ 'devices' ]:
        if device[ 'name' ] == device_name:
            return device[ 'id' ]

    print( f"Device '{device_name}' not found. Please ensure it is active." )
    return None


def handle_spotify_exception( exception ):
    if hasattr( exception, 'http_status' ) and exception.http_status == 429:
        print( "Rate limit exceeded. Pausing for 10 seconds..." )
        time.sleep( 10 )
    else:
        print( f"Spotify API error: {exception}" )


def play_album_by_name( album_name ):
    # Search for the album
    results = sp.search( q=album_name, type='album', limit=1 )
    if not results[ 'albums' ][ 'items' ]:
        print( f"No album found for '{album_name}'." )
        return

    # Get the first album's URI
    album_uri = results[ 'albums' ][ 'items' ][ 0 ][ 'uri' ]
    album_name_result = results[ 'albums' ][ 'items' ][ 0 ][ 'name' ]
    print( f"Playing '{album_name_result}'..." )

    # Play the album
    play_album( album_uri )


def pause_playback():
    try:
        sp.pause_playback()
        print( "Playback paused." )
    except Exception as e:
        print( f"Error pausing playback: {e}" )


def handle_voice_command():
    global exiting
    while not exiting:
        print( "Listening for a voice command..." )
        try:
            with m as source:
                r.adjust_for_ambient_noise( source )
                audio = r.listen( source )
                value = r.recognize_google( audio ).strip().lower()
                print( f"You said: {value}" )

                if value.startswith( "arduino play song" ):
                    song_name = value.replace( "arduino play song", "" ).strip()
                    if song_name:
                        play_song_by_name( song_name )
                    else:
                        print( "Error: No song name provided." )
                elif value.startswith( "arduino play album" ):
                    album_name = value.replace( "arduino play album", "" ).strip()
                    if album_name:
                        play_album_by_name( album_name )
                    else:
                        print( "Error: No album name provided." )
                elif value == "arduino pause":
                    pause_playback()
                elif value == "arduino exit":
                    pause_playback()
                    exiting = True
                else:
                    print( "Unrecognized command." )
        except sr.UnknownValueError:
            print( "Could not understand the audio." )
        except sr.RequestError as e:
            print( f"Speech recognition error: {e}" )


def handle_nfc_input():
    global exiting

    album_identificator = "Album URI:"
    volume_identificator = "VOLUME:"

    while not exiting:
        line = ser.readline().decode( 'utf-8', errors='replace' ).rstrip()
        if line.startswith( album_identificator ):
            text_data = line[ len( album_identificator ): ].strip()
            album_uri = text_data[ 9:-2 ]
            print( "Text Data:", album_uri )
            play_album( album_uri )
        elif line.startswith( volume_identificator ):
            volume = line[ len( volume_identificator ): ].strip()
            set_volume( int( volume ) )


if __name__ == "__main__":
    Thread( target=handle_voice_command ).start()
    Thread( target=handle_nfc_input ).start()

    # Keep the main thread alive
    try:
        while not exiting:
            time.sleep( 1 )
    except KeyboardInterrupt:
        print( "Main thread interrupted. Exiting program." )
        exiting = True
