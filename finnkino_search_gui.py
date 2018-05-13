# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import urllib.request, urllib.parse, urllib.error, re
import imageio
import math


class App(Tk):
    
    def __init__(self):
        Tk.__init__(self)
        sizex = 1550
        sizey = 800
        posx = 300
        posy = 70
        
        #this "%d" is a place holder for the values. First two are the size of the screeen nxm
        #next tho are the place GUI's left top corner will be drawn
        self.wm_geometry("%dx%d+%d+%d" % (sizex,sizey,posx,posy))
        
        self.title("Finnkino Elokuvan Haku")
        self.load_images()
        self.frame_initialize()
        

    #for loading images.
    #By loading all image in the begging and modifying them reduces the lag, if person wants to check movies in different cities
    def load_images(self):

        
        for x in range(0, (len(lines)-1)):
            
            #finding all the different titles and their pictures. Means all pictures from movies which run in Finnkino    
            title = re.findall('<Title>(.*?)</Title>',lines[x])[0]
            if(elokuva_dict.get(title) ==None):
                
                #this is http to kuva varible
                kuva = re.findall('<EventSmallImagePortrait>(.*?)</EventSmallImagePortrait>',lines[x])[0]
                
                #these are steps needed to create right kind of data type to picture
                #imageio is simple one can just get picture from web or from own computer
                im = imageio.imread(kuva)
                
                #this is to create image from bytes?
                img = Image.fromarray(im ,'RGB')
                
                #this is done so that tkinter can assign that picture to GUI
                elokuva_dict[title] = ImageTk.PhotoImage(img)
                elokuva_titlet.append(title) 
            
        
    def frame_initialize(self):
        container = ttk.Frame(self)
        #just frame things to center the frame where movies appear.
        padding_left = 130
        container.grid(column=1, row=1)
        fill_frame1 =ttk.Frame(self, width= padding_left, height=50)
        fill_frame1.grid(column=0, row=0)
        fill_frame2 =ttk.Frame(self, width= padding_left, height=300)
        fill_frame2.grid(column=0, row=1)
        city_frame =ttk.Frame(self, width= 400, height=100, padding="20 20 20 20")
        city_frame.grid(column=1, row=0)
        container.columnconfigure(0,weight=1)
        container.rowconfigure(0,weight=1)
        
            
        
        def combofunction():
            
            #get combox selected value
            city = str(city_var.get())
            
            #creating or destroying list depending if they exist, city_list is where show tag's contents are saved if selected city appears in them
            if(("city_list" in locals()) == False):
                city_list = []
            else: city_list[:] = []
            
            if(("elokuva_tiedot" in locals()) == False):
                elokuva_tiedot = []
            else: elokuva_tiedot[:]=[]
            
            #destroying when "OK" button clicked big frame in canvas will be emptied
            for child in frame_to_canvas.winfo_children():
                child.grid_forget()
                
                child.destroy()
            
            #saving info's if city is in the <Show> tag
            for x in range(0, (len(lines))):
                if(city in lines[x]):
                    city_list.append(lines[x])
                 
            
            #if no movies running -> message
            if(len(city_list)<1):
                voe_ei_text=ttk.Label(frame_to_canvas,
                text="Tällä hetkellä valitsemassanne teatterissa ei ole menossa yhtään elokuvaa")
                voe_ei_text.grid(column=0,row=0)
                
                
            for x in range(0, (len(city_list))):
                
                #getting movie information alkaa = starttime loppuu = ending time, pvm = date, teatteri= theatre
                title = re.findall('<Title>(.*?)</Title>',city_list[x])[0]
                genre = re.findall('<Genres>(.*?)</Genres>',city_list[x])[0]
                alkaa = re.findall('<dttmShowStart>\d{4}-\d{2}-\d{2}T(.*?)</dttmShowStart>',city_list[x])[0]
                loppuu = re.findall('<dttmShowEnd>\d{4}-\d{2}-\d{2}T(.*?)</dttmShowEnd>',city_list[x])[0]
                pvm = re.findall('<dttmShowStart>(.{10})',city_list[x])[0]
                teatteri= re.findall('<Theatre>(\w{1,20})',city_list[x])[0]
                
                #putting movie information to a list with movie being dictonary
                elokuva_tiedot.append({"elokuva":{"title": title, "genre":genre, "alkaa": alkaa,
                                                     "loppuu": loppuu, "teatteri":teatteri, "pvm": pvm}})
            #to create so that 5 movies in a row. Don't know it this is optimal way to do it.
            #No index out of bounds. All movies should also be in  the canvas (or in frame_to_canvas)
            iter_var = math.ceil((len(elokuva_tiedot)/elokuva_rivilkm))
            indx_var = 0
            for y in range(0, iter_var):        
                for z in range(0, elokuva_rivilkm):
                    if indx_var >= len(elokuva_tiedot):
                        break
                    
                    #beginnnig and ending time of movies. Done this way since assigning with parenthesis in text in ttk.label works in mysterious ways
                    alku_aika ="alkaa: "+ elokuva_tiedot[indx_var]["elokuva"]["alkaa"]
                    loppu_aika = "loppuu: "+ elokuva_tiedot[indx_var]["elokuva"]["loppuu"]

                    #creating frame and setting it to its place
                    elokuva_frame = ttk.Frame(frame_to_canvas, width=230, cursor="hand1")
                    elokuva_frame.grid(column=z, row= y)
                    
                    ttk.Label(elokuva_frame, image =elokuva_dict.get(elokuva_tiedot[indx_var]["elokuva"]["title"])).grid(column=0,row=0)
                    
                   
                    #getting infromation to labels and to elokuva_frame
                    ttk.Label(elokuva_frame, text=elokuva_tiedot[indx_var]["elokuva"]["title"]).grid(column=0,row=1)
                    
                    ttk.Label(elokuva_frame, text=elokuva_tiedot[indx_var]["elokuva"]["genre"]).grid(column=0,row=2)
    
                    ttk.Label(elokuva_frame, text=alku_aika).grid(column=0,row=3)
                    
                    ttk.Label(elokuva_frame, text=loppu_aika).grid(column=0,row=4)
                    
                    ttk.Label(elokuva_frame, text=elokuva_tiedot[indx_var]["elokuva"]["pvm"]).grid(column=0,row=5)
                    
                    ttk.Label(elokuva_frame, text=elokuva_tiedot[indx_var]["elokuva"]["teatteri"]).grid(column=0, row = 6)
                    
                    indx_var +=1
                    
            #paddings to elokuva_frames
            for child in frame_to_canvas.winfo_children(): child.grid_configure(padx=8, pady=8)  
            
        #some font styling to button widget
        style = ttk.Style(self)
        style.configure("TButton", font= LARGE_FONT)
              
        city_button = ttk.Button(city_frame, width= 20, text="OK", style="TButton", command=combofunction)
        city_button.grid(column = 1, row = 0)
        
        #stringvar so that it combofunction knows what value is it that the user chose
        city_var = StringVar()
        
        #must be done this way, otherwise stringvar will be garbage collected and combobox will not show "Valitse Kaupunki"
        keepvalue = city_var.get()
        
        #combobox creation. "readonly" so that user can only choose from options - no input given
        city_combo = ttk.Combobox(city_frame, textvariable=city_var, font=LARGE_FONT, state="readonly")
        
        #Cities of Finland which has Finnkino movie theatre in them
        city_combo["values"]=("Helsinki", "Vantaa", "Espoo",
        "Turku","Tampere", "Lahti", "Lappeenranta","Jyväskylä", "Pori", "Rauma","Mikkeli")
        
        #combobox's shown value - not choosable option when combobox is clicked
        city_combo.set("Valitse Kaupunki")
        city_combo.grid(column=0,row=0)
        
        
        #If one wants scrollable element one have to create a frame in which one puts canvas and then into canvas one puts a frame.
        #Frame -> Canvas -> Frame 
        #Scrollbar will be put in the first Frame (mainframe) and it will interact with canvas.
        canvas = Canvas(container, width =1130, height = 700)
        frame_to_canvas = Frame(canvas)
        
        #this things are somesort of black magic.
        #scroll to frame (container aka. the mainframe) then command tells probably that this is canvas' scroll bar for dimension y
        scrolli = Scrollbar(container, orient="vertical", command= canvas.yview)
        
        #scroll command so that scroll and canvas can interact?
        canvas.configure(yscrollcommand=scrolli.set )
        canvas.grid(column=1, row=1)
        
        #the scrollregion contains all that is in canvas
        def scrollfunction(event):
            canvas.configure(scrollregion=canvas.bbox("all"),width=1130,height=700)
        
        #Scrolling with mousewheel. -1 so that scrolling down brings canvas down.
        #int is needed probably due to pixels. There is no half a pixel?
        def mouseWheel(event):
            canvas.yview_scroll( -1*int(event.delta/120), "units")
            
              
        scrolli.grid(column=2,row=1, sticky=(N,S))
        
        
        canvas.create_window((0,0),window=frame_to_canvas, anchor='nw')
        #binding those earlier functions 
        frame_to_canvas.bind("<Configure>",scrollfunction)
        canvas.bind_all("<MouseWheel>", mouseWheel)
        

        for child in city_frame.winfo_children(): child.grid_configure(padx=5, pady=5)


    
#loading site xml and finding show tags
site = "http://www.finnkino.fi/xml/Schedule"
req = urllib.request.Request(site)
resp = urllib.request.urlopen(req)
resp_data = resp.read()
lines = re.findall('<Show>.*?</Show>', resp_data.decode(), re.DOTALL)

#some globals
elokuva_titlet = []
elokuva_dict = {}
#how many per row will be put in canvas (actually to frame in canvas)
elokuva_rivilkm = 4

#font for button and combobox
LARGE_FONT = ("Verdana", 12)
#start program
appi = App()
appi.mainloop()
        
