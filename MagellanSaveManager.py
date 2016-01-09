from tkinter import *
import os
from tkinter.ttk import *
from tkinter.filedialog import *
import shutil

class Interface(Frame):
                         
    def updateLb(self):        
        self.Lb.delete(0, END)
        shipList = self.findSbs()
        for ship in shipList :
            self.Lb.insert(END, ship)

    def addShipInSave(self,ship):
        os.path.isfile(self.file)
        shipList = []
        buff = []
        struct = []
        struct.append("<MyObjectBuilder_EntityBase xsi:type=\"MyObjectBuilder_CubeGrid\">\n")
        start = False
        for line in ship.split('\n') :
            if("MyObjectBuilder_CubeGrid" in line):
              start = True;
            if(start and not("MyObjectBuilder_CubeGrid" in line)):
                struct.append(line + "\n")
        struct.append("</MyObjectBuilder_EntityBase>\n")
        with open(self.file,"r",encoding="UTF-8") as sbsFile :
            done = False
            for line in sbsFile :
                if("<MyObjectBuilder_EntityBase" in line and not done):
                    buff.extend(struct)
                    done = True
                buff.append(line)
        with open(self.file,"w",encoding="UTF-8") as sbsFile :
            sbsFile.write("".join(buff))
        self.updateLb()

    def removeShip(self,myShipId):
        with open(self.file,"r",encoding="UTF-8") as sbsFile :
            inBase = False
            shipBuff = []
            buff = []
            for line in sbsFile :
                if("<MyObjectBuilder_EntityBase" in line):
                    shipBuff = []
                    inBase = True
                if inBase :
                    shipBuff.append(line)
                    if "<EntityId>" in line:
                        start = line.find('>') + 1 
                        end = line.find('<', start)
                        shipId = line[start:end]
                    if ("</MyObjectBuilder_EntityBase" in line):
                        inBase = False
                        if not shipId == myShipId :
                            buff.extend(shipBuff)
                elif not "</MyObjectBuilder_EntityBase" in line :
                    buff.append(line)
        with open(self.file,"w",encoding="UTF-8") as sbsFile :
            sbsFile.write("".join(buff))
            
                        
    def findSbs(self):
        os.path.isfile(self.file)
        shipList = []
        with open(self.file,"r",encoding="UTF-8") as sbsFile :
            inBase = False
            owner = 0
            structName = ""
            struct = ""
            blockCpt =0
            for line in sbsFile :
                if ("<MyObjectBuilder_EntityBase" in line):
                    inBase = True
                    owner = 0
                    blockCpt =0
                    structName = ""
                    struct = []
                    pos = ""
                    shipId = ""
                    distance = 0
                if inBase :
                    if (not "MyObjectBuilder_EntityBase" in line) :
                        struct.append(line)
                    if "<EntityId>" in line:
                        start = line.find('>') + 1 
                        end = line.find('<', start)
                        shipId = line[start:end]
                    if "<Position x" in line:
                        distance = 0
                        srcFloats = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                        for number in srcFloats:
                            pos += number
                    if("<MyObjectBuilder_CubeBlock" in line):
                        blockCpt += 1
                    if("DisplayName" in line) :
                        start = line.find('>') + 1 
                        end = line.find('<', start)
                        structName = line[start:end]
                if ("</MyObjectBuilder_EntityBase" in line):
                    inBase = False
                    if(blockCpt > 0):
                        self.ship[shipId] = "".join(struct)
                        shipList.append("ID : " + shipId +
                                              ", Name : " + structName+
                                              ", Nb blocks : " + str(blockCpt)+
                                              ", Position : " + pos + "\n")
        return shipList
                
    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, width=768, height=576, **kwargs)
        self.pack(fill=BOTH)
        self.file  =  askopenfilename(filetypes = [("sbs file","*.sbs")])
        shutil.copyfile(self.file, self.file+".back")
        self.cpt=0
        self.ship = {}        
        
        fenetre.title('MagellanSaveManager 1.0')
        
        #List
        frame =Frame(self)
        Grid.rowconfigure(frame, 0, weight=1)
        Grid.columnconfigure(frame, 0, weight=1)
        frame.grid(row=0,column=0, sticky=N+S+E+W)
        self.Lb = Listbox(fenetre, selectmode=MULTIPLE)        
        bouton_cliquer1 = Button(fenetre, text="extract",
        command=self.extract,width=80)
        bouton_cliquer2 = Button(fenetre, text="load and add to save",
        command=self.addToSave,width=80)
        self.updateLb()
        self.Lb.pack(expand=True, fill='both')
        bouton_cliquer1.pack()
        bouton_cliquer2.pack()
       

        
    def addToSave(self):
        file  =  askopenfilename(filetypes = [("sbc file","*.sbc")])
        ship = ""
        with open(file,"r",encoding="UTF-8") as shipFile :
                ship = shipFile.read() 
        self.addShipInSave(ship)

    def extract(self):
        selectedShips = [self.Lb.get(idx) for idx in self.Lb.curselection()]
        self.Lb.selection_clear(0, END)
        buff = ""
        for ship in selectedShips :
            header = "<?xml version=\"1.0\" encoding=\"utf-16\"?>\n<MyObjectBuilder_CubeGrid xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n"#<MyObjectBuilder_EntityBase xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:type=\"MyObjectBuilder_CubeGrid\">\n
            footer = "</MyObjectBuilder_CubeGrid>"            
            start = ship.find(':') + 2 
            end = ship.find(',', start)
            shipID = ship[start:end]
            start = ship.find(':', end) + 2 
            end = ship.find(',', start)
            shipName = ship[start:end]
            struct = self.ship[shipID]
            with open(shipName+".sbc","w",encoding="UTF-8") as shipFile :
                shipFile.write(header+struct+footer)
            self.removeShip(shipID)
        self.updateLb()

  




fenetre = Tk()
interface = Interface(fenetre)
interface.mainloop()
interface.destroy()
