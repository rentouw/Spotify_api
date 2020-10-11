#!/usr/bin/env python3
import json
from base64 import b64encode

import requests as req

# Parameters
clientid = "EMPTY"
clientsecret = "EMPTY"
country_code = "be"
HEADER = "EMPTY"


def acces_token(base64code):
    """
    Get Spotify acces token.

    :param base64code: Base64 encoded client_id:client_secret
    :return: access_token
    """
    post_data = {'grant_type': 'client_credentials'}
    header_data = {'Authorization': f'Basic {base64code}'}
    rtoken = req.post('https://accounts.spotify.com/api/token', data=post_data, headers=header_data)
    jtoken = json.loads(rtoken.text)
    return jtoken['token_type'] + " " + jtoken['access_token']


def get_api_token(clientid_function="EMPTY", clientsecret_function="EMPTY"):
    """
    Setup API auth token.
    :param clientid_function: Spotify client id.
    :param clientsecret_function: Spotify client secret.
    """
    global clientid, clientsecret, HEADER
    loop = True
    while loop:
        if clientid_function == "EMPTY" or clientsecret_function == "EMPTY":
            clientid = input("What is the clientid: ")
            clientsecret = input("What is the clientsecret: ")
        else:
            clientid = clientid_function
            clientsecret = clientsecret_function
        try:
            # Client id and secret encoded into base64
            byte_data = b64encode((clientid + ':' + clientsecret).encode("utf-8"))
            base64code = str(byte_data, "utf-8")
            # Get access token
            token = acces_token(base64code)
            HEADER = {'Authorization': token}
            loop = False
            print("\nClientid and Clientsecret are changed.")
        except:
            print("\n!!clientid or clientsecret are wrong !!")
    pass


def get_artist_id(name):
    """
    Get artist id from artist name.
    :param name: Artist name
    :return: Artist spotify id.
    """
    global country_code, HEADER
    rid = req.get(f'https://api.spotify.com/v1/search?q={name}&type=artist&limit=5&market{country_code}',
                  headers=HEADER)
    jid = json.loads(rid.text)
    a = jid['artists']['items']
    for iid in a:
        # Check if artist name same as search term
        if iid['name'] == name:
            return iid['id']
        # Else take first artist with genres.
        elif iid['genres']:
            return iid['id']
    pass


def get_artist_info(artist_id):
    """
    Get all the artist info.

    :param artist_id: The artist id.
    :return: The artist object.
    :rtype: https://developer.spotify.com/documentation/web-api/reference/object-model/#artist-object-full
    """
    global HEADER
    ratist = req.get(f'https://api.spotify.com/v1/artists/{artist_id}', headers=HEADER)
    return json.loads(ratist.text)


def get_top_tracks(artist_id):
    """
    Get the top most lissent to tracks.
    :param artist_id: The artist id.
    :return: top 10 tracks.
    """
    global HEADER, country_code
    rtracks = req.get(f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country={country_code}',
                      headers=HEADER)
    jtracks = json.loads(rtracks.text)
    jtracks = jtracks['tracks']
    return jtracks


def menu():
    print("*" * 25)
    print("\t1. Search artist")
    print("\t2. Options")
    print("\t3. Exit")
    print("-" * 25)
    return input("Select (1,2,3): ")


def search():
    # Ask artist name
    name = input("Artist name:")
    # Get artist id, info and top tracks
    artist_id = get_artist_id(name)
    artist_info = get_artist_info(artist_id)
    tracks = get_top_tracks(artist_id)
    # Get all the genres and put them in a list.
    genres = ', '.join(artist_info['genres'])
    print("*" * 100)
    print(f"\t Artist name: {artist_info['name']}\tPopularity: {artist_info['popularity']}")
    print(f"\t Genres: {genres}")
    print("\t Top 5 songs:")
    print(f"\t\tTitle: {tracks[0]['name']}\t Popularaty {tracks[0]['popularity']}")
    print(f"\t\tTitle: {tracks[1]['name']}\t Popularaty {tracks[1]['popularity']}")
    print(f"\t\tTitle: {tracks[2]['name']}\t Popularaty {tracks[2]['popularity']}")
    print(f"\t\tTitle: {tracks[3]['name']}\t Popularaty {tracks[3]['popularity']}")
    print(f"\t\tTitle: {tracks[4]['name']}\t Popularaty {tracks[4]['popularity']}")
    print("-" * 100)
    input("\nPress enter to continue.")
    print("\n\n")
    pass


def change_token():
    global clientid, clientsecret
    print(f"\tCurrent clientid {clientid}")
    print(f"\tCurrent clientsecret {clientsecret}")
    get_api_token()
    pass


def change_country():
    global country_code
    country_code_check = input("Pls give valid ISO 3166-1 alpha-2 country code : ")
    respons = req.get(f"https://restcountries.eu/rest/v2/alpha/{country_code_check}")
    iso_check = json.loads(respons.text)
    if respons.status_code == 200:
        country_code = iso_check['alpha2Code']
        print(f"Country code updated to {country_code_check}")
    else:
        print(f"{country_code_check} is not ISO 3166-1 valid or not a country code.")
        print(f"Using old country code : {country_code}")
    pass


def options():
    loop = True
    while loop:
        print("*" * 25)
        print("\t1. Change tokens")
        print("\t2. Change country")
        print("\t3. Exit")
        print("-" * 25)
        answer_option = input("Select (1,2,3): ")
        if answer_option == "1":
            change_token()
        elif answer_option == "2":
            change_country()
        elif answer_option == "3":
            print("\n\n\n")
            loop = False
        else:
            print("Not a valid input.")
    pass


if __name__ == '__main__':
    get_api_token()
    while 1:
        answer = menu()
        if answer == "1":
            print("\n\n\n")
            search()
        elif answer == "2":
            print("\n\n\n")
            options()
        elif answer == "3":
            print("\n\n\n")
            print("\nBye\n")
            exit()
        else:
            print("Not a valid input.")
