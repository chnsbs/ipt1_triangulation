


from Tkinter import *
from ttk import *
import tkFileDialog
import matplotlib

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import threading
import time
import csv
from scipy.interpolate import interp1d
from scipy import stats
from sklearn import datasets, linear_model
import cPickle as pickle
import copy

class Application(threading.Thread):
    def __init__(self):
        self.root = Tk()
        threading.Thread.__init__(self)
        self.z_Pos = []

        self.root.wm_title('Apllication')


        # Create Tabs on main screen
        # tab1 = Data Setup: In this tab it is possible to collect image data for \
        # new physical setup of the system.
        # tab2 = Data Preperation: In this tab it is possible to prepare the avaliable image \
        # data for image visualization.(Linear Interpolation etc.)
        # tab3 = Object Visualization: In this tab it is possible to visualize current Object under inspection

        note =  Notebook(self.root)
        tab1 = Frame(note)
        tab2 = Frame(note)
        tab3 = Frame(note)
        tab4 = Frame(note)

        note.add(tab1, text='Data Setup')
        note.add(tab2, text='Data Preparation')
        note.add(tab3, text='Object Visualization')
        note.add(tab4, text='Measurement')

        note.pack()


        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)

        ############################# Configure 'Data Setup' Tab #####################################
        # Create two frames for the tab
        self.tab1_topframe = Frame(tab1)
        self.tab1_topframe.grid(row=0)
        self.tab1_bottomframe = Frame(tab1)
        self.tab1_bottomframe.grid(row=1)
        self.initGraph()

        self.tab1_bottomframe2 = Frame(tab1)
        self.tab1_bottomframe2.grid(row=2)


        # Add a text label which explains the functions of the tab
        # explanation = """In this tab it is possible to collect image data for a new physical setup of the system.
        #                [Capture] Button: Takes a capture of lines using camera. This data will be used for line detection, extracting line positions.
        #                   """
        #message1_tab1 = Message(tab1, justify=LEFT, text=explanation); message1_tab1.pack();

        # Button for taking capture from the camere to process
        self.button_Capture = Button(self.tab1_topframe, text='Capture', command=self.capture)

        # Button for taking Z Value
        self.button_SAVE = Button(self.tab1_topframe, text='Add to Data Set', command=self.saveZPos)
        self.entry_Zpos = Entry(self.tab1_topframe)
        self.label_Zpos = Label(self.tab1_topframe, text='Enter the position in Z-Axis')

        tab1_button_Save = Button(self.tab1_bottomframe2, text='Save Setup Data', command=self.file_save)

        # Pack the widgets to make them visible to user
        self.button_Capture.grid(row=0, column=0, ipadx=20, padx=10, pady=10)
        self.entry_Zpos.grid(row=0, column=2, pady=5)
        self.label_Zpos.grid(row=0, column=1)
        self.button_SAVE.grid(row=0, column=3, ipadx=20, padx=10, pady=10)
        tab1_button_Save.grid(row=1, column=2, ipadx=20, padx=10, pady=10)

        ############################# Configure 'Data Preparation' Tab #####################################

        #panedwindow_tab2 = PanedWindow(tab2, orient=VERTICAL)
        #paned1_tab2 = LabelFrame(panedwindow_tab2, text='Loading Image Data Set', width=100, height=100)
        #panedwindow_tab2.grid(row=4, column=3)

        label1_tab2 = Label(tab2, text='Before starting Data Preparation a Data Set must be Loaded: ')
        label1_tab2.grid(row=0, column=0, ipadx=20, padx=10, pady=10)

        label2_tab2 = Label(tab2, text='Loaded Data Set must be interpolated along z-Axis: ')
        label2_tab2.grid(row=1, column=0, ipadx=20, padx=10, pady=10)


        #self.label3_tab2_Info = StringVar()
        self.label3_tab2_Info = Label(tab2, text='Waiting for data for interpolation!')
        self.label3_tab2_Info.grid(row=5, column=1, ipadx=20, padx=10, pady=10)

        button1_tab2_Load = Button(tab2, text='Load Setup Data', command=self.file_load)
        button1_tab2_Load.grid(row=0, column=1, ipadx=20, padx=10, pady=10)

        button2_tab2_Interpolate = Button(tab2, text='Interpolate', command=self.interpolateGeneralize)
        button2_tab2_Interpolate.grid(row=1, column=1, ipadx=20, padx=10, pady=10)


        ############################# Configure 'Object Visualization' Tab #####################################

        label1_tab3 = Label(tab3, text='To visualize the Object, a Data Set for the current test must be loaded and interpolated!')
        label1_tab3.grid(row=0, column=0, ipadx=5, padx=5, pady=5)
        label2_tab3 = Label(tab3, text='If everything is ok, Press the Visualize Button')
        label2_tab3.grid(row=1, column=0, ipadx=5, padx=5, pady=5)

        #button1_tab3_Capture = Button(tab3, text='Capture', command=self.capture)
        #button1_tab3_Capture.grid(row=2, column=0, ipadx=5, padx=5, pady=5)

        button2_tab3_Visualize = Button(tab3, text='Visualize', command=self.Visualize2)
        button2_tab3_Visualize.grid(row=2, column=0, ipadx=5, padx=5, pady=5)



        ############################# Configure 'Measurement' Tab #####################################
        label1_tab4 = Label(tab4, text='Maximum Values of each Line: ')
        label1_tab4.grid(row=0, column=0, ipadx=5, padx=5, pady=5)

        button1_tab4_getMax = Button(tab4, text='Measure', command=self.measurement)
        button1_tab4_getMax.grid(row=0, column=1, ipadx=5, padx=5, pady=5)



        '''
        # Buton for saving and reading datasets
        self.button_SaveDataSet = Button(self.topframe, text='Save Data Set', command=self.saveData)
        self.button_LoadDataSet = Button(self.topframe, text='Load Data Set', command=self.readData)


        # Button to interpolate fiven values
        self.button_Interpolate = Button(self.topframe, text='Interpolate', command=self.interpolateGeneralize)
        # Button to   3d plot
        self.button_3dPlot = Button(self.bottomframe2, text='Plot 3D', command=self.Visualize2)
        '''

        # Create Menu items
        self.filemenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="New", command=self.donothing)
        self.filemenu.add_command(label="Open", command=self.donothing)
        self.filemenu.add_command(label="Save", command=self.donothing)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit', command=self.root.quit)

        '''
        # Pack the widgets

        self.button_SaveDataSet.grid(row=1, column=1, ipadx=20, padx=10, pady=10)
        self.button_LoadDataSet.grid(row=1, column=2, ipadx=20, padx=10, pady=10)
        self.button_Interpolate.grid(row=0, column=5, ipadx=20, padx=10, pady=10)
        self.button_3dPlot.grid(row=1, column=1, ipadx=20, padx=10, pady=10)
        '''



        self.Zvalues = []

        # self.final[0] --> Z values
        # self.final[1] --> Line sets
        # self.final[2] --> CenterLineIndex for each Z-Value
        # self.final[3] --> Enumarated lines to the Center Line
        # self.final[4] --> Reallocation of lines for the interpolation
        self.final = [[], [], [], [], []]

        self.captr = [[], [], [], [], []]
        self.capture3d = False
        self.xPlot = []
        self.yPlot = []
        self.tempDict = {}
        self.startFlag = True

    def initGraph(self):
        self.f = Figure(figsize=(6, 4), dpi=100)
        self.a = self.f.add_subplot(111)
        self.a.plot(np.arange(len(self.z_Pos)), self.z_Pos)
        self.a.set_title("Position of a certain point of the Center Line")
        self.a.grid(True)
        self.a.autoscale(True)
        self.a.set_xlabel('X axis')
        self.a.set_ylabel('Z axis')
        self.a.axis((0, 1500, 0, 1000))
        self.canvas = FigureCanvasTkAgg(self.f, master=self.tab1_bottomframe)
        toolbar = NavigationToolbar2TkAgg(self.canvas, self.tab1_bottomframe)
        toolbar.update()
        self.canvas.get_tk_widget().pack(fill=BOTH)
        self.canvas.show()

    def getLineDetectionInstance(self, linedetection):
        self.linedetection = linedetection

    def run(self):
        print 'Gui thread started'

    def file_save(self):
        file = tkFileDialog.asksaveasfilename()
        with open(file, 'wb') as f:
            pickle.dump(self.final, f)

    def file_load(self):
        file = tkFileDialog.askopenfilename()
        with open(file, 'rb') as f:
            self.final = pickle.load(f)
            print 'Data Loaded!'
            self.label3_tab2_Info.configure(text='Data Loaded!\nReady to Interpolate!')




    def clearGraph(self):
        self.Zvalues = []
        # self.final[0] --> Z values
        # self.final[1] --> Line sets
        # self.final[2] --> CenterLineIndex for each Z-Value
        # self.final[3] --> Enumaration to the Center Line
        self.final = [[], [], [], []]
        self.xPlot = []
        self.yPlot = []

    def saveZPos(self):
        print "Entered to function: saveZPos(). Here z positions and corresponding " \
              "line informations are stored in a dictionary list"


        # Take the Z-Value and sae into a list for further usages
        Zvalue = float(self.entry_Zpos.get())
        self.Zvalues.append(Zvalue)

        # Add all informations to the final list
        # For above mentioned purpose following list is created: self.final = [[],[]]
        # self.final[0] includes z positions
        # self.final[1] includes line information for each z-Value
        # to get line dictionaries self.final[1][z-value-index][0][0]
        # Example: self.final[0][1]includes the first z-Value and self.final[1][1] \
        # corresponds to line information //
        # // for the first z-value

        self.final[0].append(Zvalue)
        self.final[1].append(self.linePositions)
        self.final[2].append(self.centerLineIndex)

        for zthItem in np.arange(len(self.final[1])):
            # for ithline in np.arange(len(self.final[1][zthItem])):
            self.xPlot.append(self.final[1][zthItem][self.final[2][zthItem]][0][100])
            self.yPlot.append(self.final[0][zthItem])

        self.a.plot(self.xPlot, self.yPlot, '*')
        self.a.autoscale(True)
        self.canvas.show()

        # if len(self.z_Pos) > 10:
        # self.initGraph()
        # print self.z_Pos

    def capture(self):
        print "Entered to function: capture()"
        # Perform Detection Process and get the line infos
        self.linedetection.process()

        if (self.linedetection.getLine() != False):
            self.linePositions = self.linedetection.getLine()
            self.centerLineIndex = self.linedetection.centerLineIndex
        elif (self.linedetection.getLine() != False):
            self.capture()


    def capture3D(self):
        print "Entered to function: capture3D()"
        self.capture3d = True

        self.linedetection.process()

        if (self.linedetection.getLine() != False):
            self.linePositions = self.linedetection.getLine()
            self.centerLineIndex = self.linedetection.centerLineIndex

            self.final[0] = None
            self.final[1] = self.linePositions
            self.final[2] = self.centerLineIndex

            self.enumareteToCenterLine()

        elif (self.linedetection.getLine() != False):
            self.capture3D()






    def _Csv_Point_Cloud(self, filename, data):
        print "Entered to function: _Csv_Point_Cloud() in Application"

        t = time.time()

        with open(filename, 'wt') as f:
            try:
                writer = csv.writer(f)
                for i in self.final[0]:
                    writer.writerow(zvalue)
                    for line in self.final[1]:
                        writer.writerow(line)
            finally:
                f.close()

        elapsed = time.time() - t
        print 'Elapsed Time for createCSV in Application: ' + str(elapsed)

        pass

    def donothing(self):
        pass

    def takeValue(self, line):

        self.line = line


    def enumareteToCenterLine(self):
        t = time.time()
        # Re-Enumaration of the Lines.
        # This function is necessary because in every new z value some lines may \
        # disappaer or appear in the capture.
        # Center Line must be 0th line:
        # . . . . -3 -2 -1 0 1 2 3 . . . .

        if(self.capture3d != True):
            enumDict = {}

            for LineSet in np.arange(len(self.final[1])):
                enumDict[(LineSet)] = {}
                for LineIndex in np.arange(len(self.final[1][LineSet])):
                    # Takes the each Lineset's center Line index and add them into \
                    # new enumarated dictionary
                    indice = int(self.final[2][LineSet]) - int(LineIndex)
                    enumDict[LineSet][indice] = self.final[1][LineSet][LineIndex]

            self.final[3] = enumDict

        elif(self.capture3d == True):
            enumDict = {}
            for LineIndex in np.arange(len(self.final[1])):
                    indice = int(self.final[2]) - int(LineIndex)
                    enumDict[indice] = self.final[1][LineIndex]

            self.final[3] = enumDict


        elapsed = time.time() - t
        print 'Elapsed Time for enumareteToCenterLine: ' + str(elapsed)


    def interpolate(self):
        # This function interpolates a point for z values
        self.InterpolationVector = {}

        if self.startFlag == True:
            for item in self.final[1][0][self.final[2][0]][0]:
                self.tempDict[item] = []
                self.startFlag = False


        # Only for center lines of each lineset
        for lineSet in np.arange(len(self.final[1])):
            for item in self.final[1][lineSet][self.final[2][lineSet]][0]:
                self.tempDict[item].append(self.final[1][lineSet][self.final[2][lineSet]][0][item])

        for item in self.tempDict:
            self.InterpolationVector[item] = interp1d(self.tempDict[item], self.final[0])

        print self.InterpolationVector[100](840)
        print self.InterpolationVector[100](850)
        print self.InterpolationVector[100](840)
        print self.InterpolationVector[100]()

        print 'ok'


    def interpolateGeneralize(self):
        t = time.time()
        self.label3_tab2_Info.configure(text='Interpolation has started!')
        # This function interpolates a point in z value

        # Initialization
        self.InterpolationDict = {}
        self.LinRegressDict = {}
        self.tempDict = {}

        # Call required functions
        self.enumareteToCenterLine()



        #Create an empty structured List to process later
        for lineSetIndex in self.final[3]:
            for lineIndex in self.final[3][lineSetIndex]:
                if not(lineIndex in self.tempDict):
                    self.tempDict[lineIndex] = {}
                    self.InterpolationDict[lineIndex] = {}
                    self.LinRegressDict[lineIndex] = {}

                    for yAxisValue in self.final[3][lineSetIndex][lineIndex][0]:
                        self.tempDict[lineIndex][yAxisValue] = []

        # doubletemp = copy.deepcopy(self.tempDict)



        for lineSetIndex in self.final[3]:
            for lineIndex in self.final[3][lineSetIndex]:
                for yAxisValue in self.final[3][lineSetIndex][lineIndex][0]:
                    if yAxisValue in self.tempDict[lineIndex]:
                        self.tempDict[lineIndex][yAxisValue].\
                            append(self.final[3][lineSetIndex][lineIndex][0][yAxisValue])

            for lineIndex in self.tempDict:
                if not(lineIndex in self.final[3][lineSetIndex]):
                    for yAxisValue in self.tempDict[lineIndex]:
                        self.tempDict[lineIndex][yAxisValue].append(None)

        for lineIndex in self.tempDict:
            for yAxisValue in self.tempDict[lineIndex]:
                notNones = []

                if not(None in self.tempDict[lineIndex][yAxisValue]):
                    # linregress() returns:
                    # slope : float     --> slope of the regression line
                    # intercept : float --> intercept of the regression line
                    # r-value : float   --> correlation coefficient
                    # p-value : float
                    # stderr : float    --> Standard error of the estimate
                    self.LinRegressDict[lineIndex][yAxisValue] = \
                        stats.linregress(self.tempDict[lineIndex][yAxisValue], self.final[0])
                else:
                    Xval = []
                    Zval = []
                    for itemIndex in np.arange(len(self.tempDict[lineIndex][yAxisValue])):
                        if self.tempDict[lineIndex][yAxisValue][itemIndex] != None:
                            Xval.append(self.tempDict[lineIndex][yAxisValue][itemIndex])
                            Zval.append(self.final[0][itemIndex])

                        #else:
                        #    pass

                    if len(Xval) >= 2:
                        self.LinRegressDict[lineIndex][yAxisValue] = stats.linregress(Xval, Zval)

                    elif len(Xval) < 2:
                        self.LinRegressDict[lineIndex][yAxisValue] = None



        elapsed = time.time() - t
        print 'Elapsed Time for interpolateGeneralize: ' + str(elapsed)
        print 'Succesfully interpolated!'
        self.label3_tab2_Info.configure(text='Successfully Interpolated!')


    def _linearRegresion(self):
        self.RegressionVector = {}
        data = {}
        # Create a tempDict for Regression instances
        if self.startFlag == True:
            for item in self.final[1][0][self.final[2][0]][0]:
                self.tempDict[item] = []
                self.startFlag = False

        # Only for center lines of each lineset
        for lineSet in np.arange(len(self.final[1])):
            for item in self.final[1][lineSet][self.final[2][lineSet]][0]:
                self.tempDict[item].append(self.final[1][lineSet]\
                                           [self.final[2][lineSet]][0][item])

        for item in self.tempDict:
            regr = linear_model.LinearRegression()
            self.RegressionVector[item] = regr.fit(self.tempDict[item], self.final[0])

        print 'ok'


    # saveData and readData
    # These functions basically saves given datasets using pickle into a file with .p extension
    # And then can read them if when they are needed.
    def saveData(self):
        pickle.dump(self.final, open("dataset.p", "wb"))
        print 'Data Saved!'

    def readData(self):
        self.final = pickle.load(open("dataset.p", "rb"))
        print 'Data Loaded!'

    def Visualize(self):

        self.capture3D()

        x = []
        y = []
        z = []
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')


        for lineIndex in self.final[3]:
            for yAxisValue in self.final[3][lineIndex][0]:

                if lineIndex in self.LinRegressDict:
                    if not(self.LinRegressDict[lineIndex][yAxisValue] is None):
                        xVal = self.final[3][lineIndex][0][yAxisValue]
                        x.append(xVal)
                        y.append(yAxisValue)

                        # Calculation of Z-Value
                        # Using linear regression tool, slope and intercept values \
                        # were calculated
                        # Z = slope * x + intercept
                        slope = self.LinRegressDict[lineIndex][yAxisValue][0]
                        intercept = self.LinRegressDict[lineIndex][yAxisValue][1]
                        z.append(slope*xVal + intercept)

                    else:
                        pass
                else:
                    pass

        #X, Y, Z = np.meshgrid(x, y, z)
        #ax.plot_wireframe(X, Y, Z, rstride=3, cstride=3)
        ax.scatter(x, y, z)
        plt.show()

    def Visualize2(self):

        self.capture3D()

        x = []
        y = []
        z = []
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        mod = 0

        for lineIndex in self.final[3]:
            for yAxisValue in self.final[3][lineIndex][0]:

                if (lineIndex in self.LinRegressDict) and (yAxisValue in self.LinRegressDict[lineIndex]):
                    if not(self.LinRegressDict[lineIndex][yAxisValue] is None) and (mod%20 == 0):
                        xVal = self.final[3][lineIndex][0][yAxisValue]
                        x.append(xVal)
                        y.append(yAxisValue)

                        # Calculation of Z-Value
                        # Using linear regression tool, slope and intercept values \
                        # were calculated
                        # Z = slope * x + intercept
                        slope = self.LinRegressDict[lineIndex][yAxisValue][0]
                        intercept = self.LinRegressDict[lineIndex][yAxisValue][1]
                        z.append(slope*xVal + intercept)

                    else:
                        pass
                else:
                    pass

                mod += 1

        #X, Y, Z = np.meshgrid(x, y, z)
        #ax.plot_wireframe(X, Y, Z, rstride=3, cstride=3)
        ax.scatter(x, y, z)
        plt.show()

        print '3D Plot'


    def measurement(self):
        z = {}

        for lineIndex in self.final[3]:
            z[lineIndex] = {}
            for yAxisValue in self.final[3][lineIndex][0]:
                if (lineIndex in self.LinRegressDict) and (yAxisValue in self.LinRegressDict[lineIndex]):
                    if not(self.LinRegressDict[lineIndex][yAxisValue] is None):
                        xVal = self.final[3][lineIndex][0][yAxisValue]
                        # Calculation of Z-Value
                        # Using linear regression tool, slope and intercept values \
                        # were calculated
                        # Z = slope * x + intercept
                        slope = self.LinRegressDict[lineIndex][yAxisValue][0]
                        intercept = self.LinRegressDict[lineIndex][yAxisValue][1]

                        z[lineIndex][yAxisValue] = slope*xVal + intercept

        maxZ = {}
        for lineIndex in z:
            if len(z[lineIndex]) > 0:
                maxxx = max(z[lineIndex].values())
                print lineIndex, '.th Line', maxxx
                maxZ[lineIndex] = maxxx









if __name__ == "__main__":
    mygui = Application()
    mygui.start()
    mygui.root.mainloop()