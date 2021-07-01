# from Predict import Predict
import cv2
import socket  # Import socket module
import pickle  # Import pickle module
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
from numpy import asarray

class ImageGenerator:
    def __init__(self, parent, posx, posy, *kwargs):
        self.parent = parent
        self.posx = posx
        self.posy = posy
        self.sizex = 200
        self.sizey = 200
        self.b1 = "up"
        self.xold = None
        self.yold = None
        self.drawing_area=tk.Canvas(self.parent,width=self.sizex,height=self.sizey)
        self.drawing_area.place(x=self.posx,y=self.posy)
        self.drawing_area.bind("<Motion>", self.motion)
        self.drawing_area.bind("<ButtonPress-1>", self.b1down)
        self.drawing_area.bind("<ButtonRelease-1>", self.b1up)
        self.button=tk.Button(self.parent,text="Classify!",width=10,bg='white',command=self.returnImage)
        self.button.place(x=self.sizex/7,y=self.sizey+20)
        self.button1=tk.Button(self.parent,text="Clear!",width=10,bg='white',command=self.clear)
        self.button1.place(x=(self.sizex/7)+80,y=self.sizey+20)


        self.label1 = tk.Label(self.parent, text='Predicted result')
        self.label1.config(font=('helvetica', 14), bg="white")
        # self.label1.place(relx = 0.75,
        #            rely = 0.45,
        #            anchor = 'center')
        self.label1.place(x = 230,
                   y = 172)

        self.image=Image.new("RGB",(200,200),(0,0,0))
        self.draw=ImageDraw.Draw(self.image)


        # SERVER IP
        self.HOST = '111.111.11.111' # server ip
        self.PORT = 50007  # Reserve a port for your service.





    def returnImage(self): 
        # create TCP/IP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.HOST, self.PORT))

        HEADERSIZE = 10
        msg = {'img': self.image}
        # pickled representation of the object
        mymsg = pickle.dumps(msg)
        mymsg = bytes(f'{len(mymsg):<{HEADERSIZE}}',"utf-8") + mymsg
        #send data
        s.sendall(mymsg)
        s.shutdown(socket.SHUT_WR)

        # recieving data(result) and print (your can change buffer size, default: 16)
        res = repr(s.recv(32).decode('utf-8'))
        print('------------------------------')
        print(f'Result: {res}')


        image1 = Image.open(f"source/{int(res[1])}.jpg")
        test = ImageTk.PhotoImage(image1)

        label1 = tk.Label(image=test, borderwidth=0)
        label1.image = test
        label1.place(x=260, y=47)

    def clear(self):
        self.drawing_area.delete("all")
        self.image=Image.new("RGB",(200,200),(0,0,0))
        self.draw=ImageDraw.Draw(self.image)

    def b1down(self,event):
        self.b1 = "down"

    def b1up(self,event):
        self.b1 = "up"
        self.xold = None
        self.yold = None

    def motion(self,event):
        if self.b1 == "down":
            if self.xold is not None and self.yold is not None:
                event.widget.create_line(self.xold,self.yold,event.x,event.y,smooth='true',width=10,fill='black')
                self.draw.line(((self.xold,self.yold),(event.x,event.y)),(255,255,255),width=10)

        self.xold = event.x
        self.yold = event.y

if __name__ == "__main__":
    root=tk.Tk()
    root.title("Digit Recognition")
    root.wm_geometry("%dx%d+%d+%d" % (400, 250, 10, 10))
    root.config(bg='white')
    ImageGenerator(root,10,10)
    root.mainloop()
