# finnkino_movies_search
GUI with python that searches movies going on in Finnkino theatres

Tried to do some Gui things with Tkinter.

How it works?
1. It downloads xml-file which is provided by Finnkino. Downloaded with urllib
2. Then it parses the file to a list with regex. One index in that list contains a string with multiple tags ie. <Show>...</Show>
3. Then with regex every list item is checked with tag title and image.
4. Image is processed for tkinter
5. Image and title is put into a dictionary with title being the key.
6. There is check if dictionary contains that image already -> all images are loaded only once
7. However all the images of the running movies are loaded -> no optimization by a city name
8. Some frames initialized...
9. Movie information extracted from lines (with regex) for ex. starting, endging time, movie theatre and so on..
10. Image and information is put into a frame which is put into a frame that lies in canvas which lies in frame (mainframe)
11. information->frame->bigger frame->canvas->mainframe
12. Combobox's city value decides which movies are shown when user click "OK" button

Problems
-frame sizes are decided by the widest element. Sometimes this can create problem with some elements going of the screen.
-> could have added a horizontal slide
-Could have added more functions. I tried to add to a movieframe function which opens a tab in browser and shows the movie in Finnkino site.
-Not much customization done, this is pretty dull looking gui.
