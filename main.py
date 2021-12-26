from PIL import Image as PIL_Image
from PIL import ImageTk as PIL_ImageTK


import cv2
import tkinter
from tkinter import TOP, LEFT, NW, HORIZONTAL, N
from tkinter.filedialog import askopenfile

# import copy_move_detection as cmd
import error_level_analysis as ela
import noise_level_analysis as nla
import copy_move_detection as cmd


# Initializing main window
MainWin = tkinter.Tk()

# Getting screen dimentions and setting default state of window as zoomed
ScreenWidth, ScreenHeight = MainWin.winfo_screenwidth(), MainWin.winfo_screenheight()
MainWin.state('zoomed')

# Setting window title
MainWin.title("Digital Image Manipulation Detection")

# Browse option function
ImagePath = None
CurrentImage = None
def BrowseImage():
    global ImagePath, CurrentImage

    # Opening the browse window and taking only files of type ".jpeg", ".jpg", and ".png"
    file = tkinter.filedialog.askopenfile(mode='r', filetypes=[('Image Files', ['*.jpg', '*.jpeg', '*.png'])])
    if file is None:
        ImagePath = None
    else:
        ImagePath = file.name

    # Return if image path is None
    if ImagePath is None:
        return

    # Reading the image
    CurrentImage = cv2.imread(ImagePath)

    # As new image is read, clear the Frames and show the image
    Pack_Forget_All()
    ShowImage()


# Function for calling the copy-move detection algorithm.
def Call_CopyMoveDetection(*args):
    global CurrentImage, CMDFrame, epsScale

    # Return if no image
    if CurrentImage is None:
        print("Calling copy-move detection: No current image found.")
        return

    # Packing only the copy-move detection algo's frame
    Pack_Forget_All()
    CMDFrame.pack()

    # cmd.CopyMoveDetection(CurrentImage.copy())
    # ShowImage(path="resImg_LinedImg.jpg")

    # Finding the forgery (copy-move) in the image
    imgObject = cmd.Detect(CurrentImage)
    imgObject.siftDetector()
    eps = int(epsScale.get())       # 0-500

    forgeryImage = imgObject.locateForgery(eps, 2)

    # Showing the forgery image
    ShowImage(Image=forgeryImage)


# Function for calling the error level analysis detection algorithm.
def Call_ErrorLevelAnalysis(*args):
    global CurrentImage, QualityScale, ELAFrame

    # Return if no image
    if CurrentImage is None:
        print("Calling ELA: No current image found.")
        return

    # Packing only the error level analysis's frame
    Pack_Forget_All()
    ELAFrame.pack()

    # Calculating the error level analysis output image
    ELA_OutputImage = ela.ErrorLevelAnalysis(CurrentImage.copy(), int(QualityScale.get()), int(ErrorScaleScale.get()))

    # Showing the output image
    ShowImage(Image=ELA_OutputImage)


# Function for calling the noise level analysis detection algorithm.
def Call_NoiseLevelAnalysis(*args):
    global CurrentImage, NoiseAmplitudeScale, NLAFrame

    # Return if no image
    if CurrentImage is None:
        print("Calling NLA: No current image found.")
        return

    # Packing only the noise level analysis's frame
    Pack_Forget_All()
    NLAFrame.pack()

    # Calculating the noise level analysis output image
    NLA_OutputImage = nla.NoiseLevelAnalysis(CurrentImage.copy(), 5, int(NoiseAmplitudeScale.get()))

    # Showing the output image
    ShowImage(Image=NLA_OutputImage)


# function for resizing the image to fit in image label
def ResizeImage(img):
    global ImageLabel, ImageLabelDims
    img_width, img_height = img.size

    # If image is smaller than the frame, do nothing
    if img_width < ImageLabelDims[0] and img_height < ImageLabelDims[1]:
        return img

    # Image width by Height ratio
    img_ratio = img_width / img_height

    # Calculating new width and height by fitting the width
    new_width = int(ImageLabelDims[1] * img_ratio)
    new_height = int(new_width / img_ratio)
    # Checking if image now fits the image label.
    # If fits, then resize the image and return.
    if new_width < ImageLabelDims[0] and new_height < ImageLabelDims[1]:
        img = img.resize((new_width, new_height), PIL_Image.BILINEAR)
        return img

    # Calculating new width and height by fitting the height
    new_height = int(ImageLabelDims[0] / img_ratio)
    new_width = int(new_height * img_ratio)
    # Checking if image now fits the image label.
    # If fits, then resize the image and return.
    if new_width < ImageLabelDims[0] and new_height < ImageLabelDims[1]:
        return img.resize((new_width, new_height), PIL_Image.BILINEAR)

    return img


# Function for displaying the image
def ShowImage(Image=None, path=None):
    global ImagePath, ImageLabel

    # Setting Image and path
    if Image is not None:
        cv2.imwrite("ImageToShow.jpg", Image)
        path = "ImageToShow.jpg"
    else:
        if path is None:
            path = ImagePath
        if path is None:
            return

        # Reading and saving image for other algorithms
        cvImg = cv2.imread(ImagePath)
        cv2.imwrite("ImageToShow.jpg", cvImg)

    # Reading the image, resizing it, and showing the image
    img = PIL_Image.open(path).convert('RGB')
    img = ResizeImage(img)
    img = PIL_ImageTK.PhotoImage(img)
    ImageLabel.config(image=img)
    ImageLabel.image=img


# Function for forgetting all algorithms' frame pack.
def Pack_Forget_All():
    ELAFrame.pack_forget()
    NLAFrame.pack_forget()
    CMDFrame.pack_forget()


#################################################################################
# Creating menu bar
menu = tkinter.Menu(MainWin)
MainWin.config(menu=menu)
# File menu
filemenu = tkinter.Menu(menu, tearoff="off")
menu.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='Open Image', command=BrowseImage)
filemenu.add_separator()
filemenu.add_command(label='Exit', command=MainWin.quit)
# View Menu
view_menu = tkinter.Menu(menu, tearoff="off")
menu.add_cascade(label='View', menu=view_menu)
view_menu.add_command(label='Copy-Move', command=Call_CopyMoveDetection)
view_menu.add_command(label='ELA', command=Call_ErrorLevelAnalysis)
view_menu.add_command(label='NLA', command=Call_NoiseLevelAnalysis)
#################################################################################

#################################################################################
# Creating label for displaying image in the canvas
ImageLabelDims = [int(ScreenWidth*0.7)-80, ScreenHeight-80]
ImageLabelFrame = tkinter.Frame(MainWin)
ImageLabel = tkinter.Label(ImageLabelFrame, width=ImageLabelDims[0], height=ImageLabelDims[1])
ImageLabel.pack(side=TOP, anchor=NW, padx=20)
ImageLabelFrame.pack(side=LEFT)
#################################################################################

#################################################################################
# Creating ELA sliders' frame
ELAFrameDims = [int(ScreenWidth*0.3)-80, ScreenHeight - 80]
ELAFrame = tkinter.Frame(MainWin, width=ELAFrameDims[0], height=ELAFrameDims[1])

ELALabel = tkinter.Label(ELAFrame, text="Error Level Analysis", font=('Helvetica bold', 16))
ELALabel.pack(side=TOP, anchor=NW, pady=(200, 0))

QualityLabel = tkinter.Label(ELAFrame, text="JPEG Quality", font=('Helvetica bold', 14))
QualityLabel.pack(side=TOP, anchor=NW, pady=(30, 0))
QualityScale = tkinter.Scale(ELAFrame, from_=1, to=100, orient=HORIZONTAL, length=250, font=('Helvetica bold', 13), command=Call_ErrorLevelAnalysis)
QualityScale.set(90)
QualityScale.pack(side=TOP, anchor=NW, pady=(5, 0))

ErrorScaleLabel = tkinter.Label(ELAFrame, text="Error Scale", font=('Helvetica bold', 14))
ErrorScaleLabel.pack(side=TOP, anchor=NW, pady=(30, 0))
ErrorScaleScale = tkinter.Scale(ELAFrame, from_=0, to=100, orient=HORIZONTAL, length=250, font=('Helvetica bold', 13), command=Call_ErrorLevelAnalysis)
ErrorScaleScale.set(20)
ErrorScaleScale.pack(side=TOP, anchor=NW, pady=(5, 0))

ELAFrame.pack(side=LEFT, anchor=N)
ELAFrame.pack_forget()
#################################################################################

#################################################################################
# Creating NLA sliders' frame
NLAFrameDims = [int(ScreenWidth*0.3)-80, ScreenHeight - 80]
NLAFrame = tkinter.Frame(MainWin, width=NLAFrameDims[0], height=NLAFrameDims[1])

NLALabel = tkinter.Label(NLAFrame, text="Noise Level Analysis", font=('Helvetica bold', 16))
NLALabel.pack(side=TOP, anchor=NW, pady=(200, 0))

NosieAmplitude = tkinter.Label(NLAFrame, text="Noise Amplitude", font=('Helvetica bold', 14))
NosieAmplitude.pack(side=TOP, anchor=NW, pady=(30, 0))
NoiseAmplitudeScale = tkinter.Scale(NLAFrame, from_=1, to=100, orient=HORIZONTAL, length=250, font=('Helvetica bold', 13), command=Call_NoiseLevelAnalysis)
NoiseAmplitudeScale.set(1)
NoiseAmplitudeScale.pack(side=TOP, anchor=NW, pady=(5, 0))

NLAFrame.pack(side=LEFT, anchor=N)
NLAFrame.pack_forget()
#################################################################################


#################################################################################
# Creating copy-move detction sliders' frame
CMDFrameDims = [int(ScreenWidth*0.3) - 80, ScreenHeight - 80]
CMDFrame = tkinter.Frame(MainWin, width=CMDFrameDims[0], height=CMDFrameDims[1])

CMDLabel = tkinter.Label(CMDFrame, text="Copy-Move Detection", font=('Helvetica bold', 16))
CMDLabel.pack(side=TOP, anchor=NW, pady=(200, 0))

epsAmplitude = tkinter.Label(CMDFrame, text="EPS", font=('Helvetica bold', 14))
epsAmplitude.pack(side=TOP, anchor=NW, pady=(30, 0))
epsScale = tkinter.Scale(CMDFrame, from_=1, to=200, orient=HORIZONTAL, length=250, font=('Helvetica bold', 13), command=Call_CopyMoveDetection)
epsScale.set(60)
epsScale.pack(side=TOP, anchor=NW, pady=(5, 0))

CMDFrame.pack(side=LEFT, anchor=N)
CMDFrame.pack_forget()
#################################################################################


# Running the GUI
MainWin.mainloop()
