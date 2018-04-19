#!/usr/bin/env python
#youtube test
# import pafy
# myvid = pafy.new("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
# print(myvid.author)

# plurl = "https://www.youtube.com/playlist?list=PL634F2B56B8C346A2"
# playlist = pafy.get_playlist(plurl)
# print(playlist['title'])
from_index = None
while from_index is None or from_index > 10:
    try:
        from_index = int(input("Input from index, max size : {} ".format(10)))
        print(from_index)
    except ValueError:
        print("Enter a integer Value in range 0, {}".format(10))