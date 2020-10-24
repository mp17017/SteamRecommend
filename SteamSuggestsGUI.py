#GUI imports
from PIL import Image, ImageTk
import tkinter as tk
#Data Scrape imports
from requests import get as req
from bs4 import BeautifulSoup as soup
#Machine Learning Program


##GUI IMPLEMENTATION##############################################

class BkgrFrame(tk.Frame):
    def __init__(self, parent, file_path, width, height):
        super(BkgrFrame, self).__init__(parent, borderwidth=0, highlightthickness=0)

        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.pack()

        pil_img = Image.open(file_path)
        self.img = ImageTk.PhotoImage(pil_img.resize((width, height), Image.ANTIALIAS))
        self.bg = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)

    def add(self, widget, x, y):
        canvas_window = self.canvas.create_window(x, y, anchor=tk.NW, window=widget)
        return widget
    
#Get CSV of user data######################################################### 
    
class user:
    """Returns a USER object"""

    def __init__(self, s64=None, sid=None):
        if(s64 != None):
            s64 = str(s64)
            if(len(s64) != 17):
                raise Exception('The Steam64 provided is invalid')
            aft = f'profiles/{s64}/'
        elif(sid != None):
            sid = str(sid)
            aft = f'id/{sid}/'
        else:
            raise Exception('Invalid user parameters')

        self.url = f'http://steamcommunity.com/{aft}'
        self.soupMain = soup(req(self.url).text, 'html.parser')
        if('error' in self.soupMain.title.text.lower()):
            raise Exception('Error retrieveing Steam Profile')
        self.soupDate = soup(req(f'{self.url}badges/1/').text, 'html.parser')
        self.soupBadges = soup(req(f'{self.url}badges/').text, 'html.parser')
        self.soupGames = soup(req(f'{self.url}games/?tab=all').text, 'html.parser')
        self.persona = self.getPersona()
        self.games = self.getGames()

    def printAll(self):
        """For debugging, prints all items in the USER object."""
        [print(f'{a}: {self.__getattribute__(a)}') for a in dir(self) if not a.startswith('__') and not a.startswith('soup') and not callable(self.__getattribute__(a)) and a != 'req']
        print()
        

    def getPersona(self):
        """Will return the display-name (persona) of the user."""
        elem = self.soupMain.find('span', class_='actual_persona_name')
        persona = elem.text
        return persona

    def getGames(self):
        """Will return the recently games of the user."""
        recents = []
        allGames = self.soupMain.findAll('div', class_='recent_game_content')
        with open('SteamUserDATA.csv','wb') as file:
            UN = 'Games\n'
            file.write(UN.encode(encoding='UTF-8'))
            for game in allGames:
                parElem = game.find('div', class_='game_name')
                nameElem = parElem.find('a', class_='whiteLink')
                recent = nameElem.text.strip() + '\n'
                recents.append(recent)
                bytesC = recent.encode(encoding='UTF-8')
                file.write(bytesC)
        return recents

class Game:
    """Will return a game object, with various information about each game."""

    def __init__(self, inst):
        """Will return a game object, with various information about each game."""
        self.appid = inst['appid']
        self.name = inst['name']


    
##Methods
    
def setidNumber():
    idNumber = str(steam_id.get())
    #print(idNumber)
    prof = user(s64=idNumber)   
    prof.getGames()

def runML():
    import Project1
    exec(Project1.py)

def getidNumber(self):
    return self.idNumber

if __name__ == '__main__':

    #GUI
    IMAGE_PATH = 'logo.png'
    WIDTH, HEIGTH = 800, 400
    root = tk.Tk()
    root.geometry('{}x{}'.format(WIDTH, HEIGTH))
    root.title("SteamNet Suggestion Engine")
    bkrgframe = BkgrFrame(root, IMAGE_PATH, WIDTH, HEIGTH)
    bkrgframe.pack()

    ##WIDGETS
    desc = bkrgframe.add(tk.Label(root, text="Enter your Steam ID# to begin.",bg="GRAY", width = 24),290,265)
    steam_id = bkrgframe.add(tk.Entry(root), 300, 300)
    button1 = bkrgframe.add(tk.Button(root, text="Retrieve Data", command=setidNumber), 300, 335)
    button2 = bkrgframe.add(tk.Button(root, text="Display Data", command=runML), 410, 335)
    #RUN GUI
    
    #76561197988747765
    root.mainloop()