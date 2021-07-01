import torch
from DigitNet import DigitNet
import cv2
import numpy as np
from PIL import Image
from torch.autograd import Variable
import torchvision.transforms as transforms


class Predict:
    def __init__(self):
        self.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None


# --------------------------------------------------------------------------------
# Load model & weigths
    def load_model(self):        
        self.model = DigitNet().to(self.DEVICE)
        self.model.load_state_dict(torch.load("mnist_cnn.pt"))
        self.model.eval()

 
    def transform(self):
        imsize = 28
        loader = transforms.Compose([transforms.Resize((28,28),interpolation=Image.NEAREST),
                                    transforms.Grayscale(num_output_channels=1),
                                    transforms.ToTensor(),
                                    transforms.Normalize((0.1307,), (0.3081,))
                                    ])

        # self.image = Image.fromarray(self.image)#  Image.open(image_name)
        self.image = loader(self.image).float()
        self.image = Variable(self.image, requires_grad=True)
        self.image = self.image.unsqueeze(0).cuda()  
 


    # --------------------------------------------------------------------------------

    def prediction(self, img):

        self.load_model()
        self.image = img
        self.transform()

        with torch.no_grad():
            x = self.image.to(device=self.DEVICE)
            output = self.model(x)
  
            pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
            return pred