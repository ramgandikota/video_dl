#!/usr/bin/env python
#Youtube downloader
import pafy
import os
def create_dir(folder_name, dest_folder=None):
    if dest_folder == None:
        dest_folder = os.getcwd()
    if not os.path.exists(dest_folder + '/' + folder_name):
        os.makedirs(dest_folder + '/' + folder_name)
        return 1
    else:
        print("Directory already exists")
        return 0

def move_file(from_dir, to_dir, filename):
    os.rename(from_dir + "/" + filename, to_dir + "/" + filename)

def promptyn(message):
    inp = input(message + ", Enter Yes (y), No (n) :").lower()
    if inp == 'y':
        print("Validated")
        return True
    else:
        print("Not Validated")
        return False

def download_video(video_item, silent=False):
    print("{}, {}, {}".format(video_item.title, video_item.viewcount, video_item.duration))
    source = video_item.getbest()
    if not silent:
        user_prmpt = input("Size is {}, Download? Yes(1), No(2)".format(source.get_filesize())).lower()
        while user_prmpt not in "12":
            user_prmpt = input("Size is {}, Download? Yes(1), No(2)".format(source.get_filesize())).lower()
        if user_prmpt == "2":
            return
    # Download the video
    try:
        filename = source.download(quiet=silent) 
    except FileExistsError:
        return

def get_playlist_details(playlist_url): # ="https://www.youtube.com/playlist?list=PLkDaE6sCZn6Gl29AoE31iwdVwSG-KnDzF"
    print("Getting Playlist Details of " +  playlist_url)
    if not playlist_url.startswith('https:'):
        playlist_url = "https://www.youtube.com/playlist?list=" + playlist_url
        if not promptyn("Valid URL: " + playlist_url):
            print('Invalid input')
            return

    playlist = pafy.get_playlist(playlist_url)
    print("Playlist Title: {}, Videos: {}".format(playlist['title'], len(playlist['items'])))
    return playlist, playlist['title'], len(playlist['items'])

def grab_playlist(playlist, from_index=0, to_index=None, dest_folder=None, silent=False, action=None):
    if dest_folder is None:
        dest_folder = os.getcwd()
    dest_folder = dest_folder.replace("\\", "/")
    
    pl_size = len(playlist['items'])
    print("Playlist Details: \n\t{}, \n\t Video Count : {}".format(playlist['title'], pl_size))

    # Set & Validate Action
    if action is None:
        while(action):
            action = input('Enter Action \n\tDownload PlayList ({}), \n\tList Video Names ({}), \n\tVideo Count ({})'.format("D", "L", "C"))
            if action not in 'dlc':
                print("Unknown input {}".format(action), end=", ")
                action = None
    
    # Set & Validate Indices
    if to_index is None or to_index >= pl_size:
        to_index = pl_size - 1

    while from_index is None or from_index >= pl_size:
        try:
            from_index = int(input("Input from index, max size : {} ".format(to_index)))
        except ValueError:
            print("Enter a integer Value in range 0, {}".format(to_index))
			
    if not silent:
        print('From Index: {}, To Index : {}'.format(from_index, to_index)) 

    # Perform action from from_index -> to_index 
    for i in range(from_index, to_index+1):
        item = playlist['items'][i]['pafy']
        if action.startswith('d'):
            filepath  = os.getcwd().replace("\\","/") + "/" + item.title;
            if os.path.exists(filepath + ".mp4") or os.path.exists(filepath + ".webm"):
                continue
            download_video(item, silent)
        else:
            print("{}: {}, {}, {}".format(i, item.title, item.viewcount, item.duration))
        
    print("List count: {}".format(to_index+1 - from_index)) 


def grab_playlistbyURL(playlist_url, from_index=0, to_index=None, dest_folder=None, silent=False, action=None): #="https://www.youtube.com/playlist?list=PLkDaE6sCZn6Gl29AoE31iwdVwSG-KnDzF"
    if dest_folder == None:
        dest_folder = os.getcwd()
    dest_folder = dest_folder.replace("\\", "/")
    if not playlist_url.startswith('https:'):
        playlist_url = "https://www.youtube.com/playlist?list=" + playlist_url
        if not promptyn("Valid URL: " + playlist_url):
            print('Invalid input')
            return    
    playlist = pafy.get_playlist(playlist_url)
    print("Playlist Title: {}, Videos: {}".format(playlist['title'], len(playlist['items'])))
    if action == None:
        action = input("Enter Action:  Download PlayList (D), List Video Names (L), Video Count (C): ").lower()
    if to_index == None:
        to_index = len(playlist['items']) - 1
    print('From Index: {}, To Index : {}'.format(from_index, to_index))
    
    if action.startswith('d'):
        # create_dir(playlist['title'])
        for i in range(from_index, to_index+1):
            item = playlist['items'][i]['pafy']
            print("{}: {}, {}, {}".format(i, item.title, item.viewcount, item.duration))
            source = item.getbest()
            if not silent:
                user_prmpt = input("Size is {}, Download? Yes(1), No(2), Yes to All(3), No to All(4)".format(source.get_filesize()))
                if user_prmpt == '4':
                    break
                elif user_prmpt == '3':
                    silent = True
                elif user_prmpt == '2':
                    continue
            try:
                filename = source.download() 
            except FileExistsError:
                continue
            # move_file(os.getcwd().replace("\\","/"), dest_folder + "/" + playlist['title'], filename)

    elif action.startswith('l'):
        print('Playlist :  %s' % playlist['title'])
        for i  in range(from_index, to_index+1):
            item = playlist['items'][i]['pafy']
            print("{}: {}, {}, {}".format(i, item.title, item.viewcount, item.duration))
        print('List Count: {}'.format(to_index + 1))
    elif action.startswith('c'):
        print('List Count: {}'.format(to_index + 1))
    else:
        print("Invalid input try again")

#PLBAGcD3siRDguyYYzhVwZ3tLvOyyG5k6K
# grab_playlist("PLBAGcD3siRDguyYYzhVwZ3tLvOyyG5k6K", 25)#, dest_folder'C:/Users/jcyar/Videos/4K Video Downloader/Convolutional Neural Networks (Course 4 of the Deep Learning Specialization) - YouTube')
# plurl = "https://www.youtube.com/playlist?list=PL634F2B56B8C346A2"
# playlist = pafy.get_playlist(plurl)
# print(playlist['title'])