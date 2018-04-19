#!/usr/bin/env python
# Multi 
from __future__ import print_function       #should be on the top
import threading
import time
import youtube_download as yd

class YTThread(threading.Thread):
    playlist_url = ""
    from_index = None
    to_index = None

    def set(self, playlist, from_index, to_index):
        self.playlist, self.from_index, self.to_index =  playlist, from_index, to_index

    def run(self):
        print("{} started!, URL:{} [{} - {}]".format(self.getName(), self.playlist_url, self.from_index, self.to_index))              # "Thread-x started!"
        yd.grab_playlist(self.playlist, self.from_index, self.to_index, silent=True, action="d")
        print("{} finished!".format(self.getName()))             # "Thread-x finished!"

if __name__ == '__main__':
    # plurl = "PLBAGcD3siRDittPwQDGIIAWkjz-RucAc7"
    pl_url = input("Enter Playlist URL: ")
    playlist, pl_name, pl_size = yd.get_playlist_details(pl_url)
    for x in range(3):      
        mythread = YTThread(name = "{} Thread-{}".format(pl_name , x + 1))  # Instantiate a thread and pass a unique ID to it
        mythread.set(playlist,  int((pl_size*x)/3), int(((pl_size*(x+1))/3)-1))
        mythread.start()                                                    #     ...Start the thread
