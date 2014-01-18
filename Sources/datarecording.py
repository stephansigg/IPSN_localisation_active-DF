#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: writeToFile
# Description: USRP source write to file

##################################################

from PyQt4 import Qt
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from gnuradio.qtgui import qtgui
from optparse import OptionParser
import sip
import sys
import threading
import time
import math 
###################################
### Orange:
import orange, orngTree
######################
# import for svm:
from Orange.classification import svm
from Orange.evaluation import testing, scoring
######################
# For Confusion matrix:
import orngTest, orngStat
######################
import Orange

##############################
### for the queue
from collections import deque
import collections
import numpy

#import scipy
import scipy
from scipy import stats

import copy
from array import *
#import array
import wx


###########################
### plot features
#from multiprocessing import Process
from matplotlib.pyplot import plot, show


#Todo: integrate the training of classifiers as already done in python
# Todo: Then, take the sample data, extract relevant features and use them for classification according to the previously sampled features.
# Todo: Then, output the classification
# Todo: Then, to make this more convenient, add a training mode, in which specific contexts can be written to then train the classifiers.


class top_block(gr.top_block, Qt.QWidget):
	def __init__(self):
		gr.top_block.__init__(self, "writeToFile")
		Qt.QWidget.__init__(self)
		self.setWindowTitle("writeToFile")
		self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
		self.top_scroll_layout = Qt.QVBoxLayout()
		self.setLayout(self.top_scroll_layout)
		self.top_scroll = Qt.QScrollArea()
		self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
		self.top_scroll_layout.addWidget(self.top_scroll)
		self.top_scroll.setWidgetResizable(True)
		self.top_widget = Qt.QWidget()
		self.top_scroll.setWidget(self.top_widget)
		self.top_layout = Qt.QVBoxLayout(self.top_widget)
		self.top_grid_layout = Qt.QGridLayout()
		self.top_layout.addLayout(self.top_grid_layout)
		self.bufferRE = collections.deque(400*[0], 400) # init buffer of 400 entries, max length 400
		self.bufferIM = collections.deque(400*[0], 400) # init buffer of 400 entries, max length 400
		

		##################################################
		# Variables
		##################################################
		self.variable_function_probe_1 = variable_function_probe_1 = 0
		self.variable_function_probe_0 = variable_function_probe_0 = 0
		self.samp_rate = samp_rate = 320000
		self.receiveFrequency = receiveFrequency = 900000000

		##################################################
		# Blocks
		##################################################
		self.gr_probe_signal_f_1 = gr.probe_signal_f()
		self.gr_probe_signal_f_0 = gr.probe_signal_f()
		def _variable_function_probe_1_probe():
			while True:
				val = self.gr_probe_signal_f_1.level()
				try: self.set_variable_function_probe_1(val)
				except AttributeError, e: pass
				time.sleep(1.0/(100)) # Sample rate 100 Hz
		# starts the thread that samples the signal continuously
		_variable_function_probe_1_thread = threading.Thread(target=_variable_function_probe_1_probe)
		_variable_function_probe_1_thread.daemon = True
		_variable_function_probe_1_thread.start()
		def _variable_function_probe_0_probe():
			while True:
				val = self.gr_probe_signal_f_0.level()
				try: self.set_variable_function_probe_0(val)
				except AttributeError, e: pass
				time.sleep(1.0/(100)) # Sample rate 100 Hz
		# starts the thread that samples the signal continuously
		_variable_function_probe_0_thread = threading.Thread(target=_variable_function_probe_0_probe)
		_variable_function_probe_0_thread.daemon = True
		_variable_function_probe_0_thread.start()
		### TODO: Write values read from the channel continuously into a buffer
		### TODO: read out the buffer continuously in another thread for classification
		### TODO: output the classification
		def _variable_classification():
			while True:
				# TODO: do classification here
				classification = self.get_classification()
				# TODO: Write out classification
				time.sleep(1.0/(2)) # One classification every 0.5 seconds
		# starts the thread that samples the signal continuously
		_variable_classification_thread = threading.Thread(target=_variable_classification)
		_variable_classification_thread.daemon = True
		_variable_classification_thread.start()

		def _variable_featureVisualisation(*args):
		  while True:
		    for data in args:
		      plot(data)
		      show()
		    time.sleep(1.0/(2))
		_variable_featureVisualisation_thread = threading.Thread(target=_variable_featureVisualisation)
		_variable_featureVisualisation_thread.daemon = True
		_variable_featureVisualisation_thread.start()
		#p = Process(target=plot_graph, args=([1, 2, 3],))
		#p.start()
		
		self.uhd_usrp_source_0 = uhd.usrp_source(
			device_addr="",
			stream_args=uhd.stream_args(
				cpu_format="fc32",
				channels=range(1),
			),
		)
		self.uhd_usrp_source_0.set_samp_rate(samp_rate)
		self.uhd_usrp_source_0.set_center_freq(receiveFrequency, 0)
		self.uhd_usrp_source_0.set_gain(20, 0)
		self.qtgui_sink_x_0 = qtgui.sink_c(
			1024, #fftsize
			firdes.WIN_BLACKMAN_hARRIS, #wintype
			0, #fc
			samp_rate, #bw
			"QT GUI Plot", #name
			True, #plotfreq
			True, #plotwaterfall
			True, #plottime
			True, #plotconst
		)
		self.qtgui_sink_x_0.set_update_time(1.0 / 10)
		self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)
		self.top_layout.addWidget(self._qtgui_sink_x_0_win)
		self.gr_complex_to_float_0 = gr.complex_to_float(1)

		##################################################
		# Connections
		##################################################
		self.connect((self.uhd_usrp_source_0, 0), (self.gr_complex_to_float_0, 0))
		self.connect((self.gr_complex_to_float_0, 0), (self.gr_probe_signal_f_0, 0))
		self.connect((self.gr_complex_to_float_0, 1), (self.gr_probe_signal_f_1, 0))
		self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_sink_x_0, 0))


	def get_variable_function_probe_1(self):
		return self.variable_function_probe_1

	def set_variable_function_probe_1(self, variable_function_probe_1):
		self.variable_function_probe_1 = variable_function_probe_1
		# print output for real part		
		fileRE = open ('outputRE', 'a')
		fileRE.write(str(self.variable_function_probe_1) + '\n')
		fileRE.close()
		# TODO: write the value also into a buffer (size: 200 values for continuous classification) But: Could also be longer.
		#print self.variable_function_probe_1
		self.bufferRE.pop() #pop(delete) rightmost entry
		self.bufferRE.appendleft(str(self.variable_function_probe_1)) # append str(self.variable_function_probe_1) to the left and shift the rest

	def get_variable_function_probe_0(self):
		return self.variable_function_probe_0

	def set_variable_function_probe_0(self, variable_function_probe_0):
		self.variable_function_probe_0 = variable_function_probe_0
		# print output for imaginary part
		fileIM = open ('outputIM', 'a')
		fileIM.write(str(self.variable_function_probe_0) + '\n')
		fileIM.close()
		self.bufferIM.pop() #pop(delete) rightmost entry
		self.bufferIM.appendleft(str(self.variable_function_probe_0)) # append str(self.variable_function_probe_0) to the left and shift the rest

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
		self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate)

	def get_receiveFrequency(self):
		return self.receiveFrequency

	def set_receiveFrequency(self, receiveFrequency):
		self.receiveFrequency = receiveFrequency
		self.uhd_usrp_source_0.set_center_freq(self.receiveFrequency, 0)
		
	def get_classification(self):
		# copy buffer to work with the data (would otherwise change too fast)
		output=list(self.bufferRE)
		zeroCrossRE=0.0
		maxPosRE=0.0
		sumDifferenceRE=0.0
		maxCounterRE=0.0
		directionchange=0.0
		DirChanzeroCross=0.0   #number of direction change
          	Sum = 0.0
		# type conversion: after the initialisation, the data in the buffer is not of the same type
		for i in range(0,400):
		  output[i]=float(output[i])
		  # calcualte zero crossings
		  if i>0:
		    if output[i-1]<0 and output[i]>0:
		      zeroCrossRE+=1
		    elif output[i-1]>0 and output[i]<0:
		      zeroCrossRE+=1  			#this can do by output[i]*output[i+1]<0
		  # prepare calculation of diff (difference of successing maxima)
		  if i>1:
		    if output[i-2] < output[i-1] and output[i-1] < output[i]:
		      maxCounterRE+=1
		      sumDifferenceRE+=i-maxPosRE
		      maxPosRE=i
		# calculate diff
		if maxCounterRE == 0.0:
		  diffRE=0.0
		else:
		  diffRE = sumDifferenceRE/maxCounterRE
		# calculate mean
		meanRE = numpy.mean(output)
		#calculate median
		medianRE = numpy.median(output)
		# calculate variance
		varRE = numpy.var(output)
		#calculate Third Central Moment
		TCM = scipy.stats.moment(output, moment=3, axis=0)
		# calculate rms
		rmsRE =	numpy.sqrt((numpy.sum(output))*(numpy.sum(output))/400)
		#calculate Max, min
		minRE = numpy.min(output)		
		# calculate count (how often within 10% of max)
		maxRE = numpy.max(output)
		tenPercentMaxRE = maxRE*0.9
		countRE=0.0
		for i in range(0,400):
		  if output[i]>tenPercentMaxRE:
		    countRE+=1
		#calculate direction change
		for i in range(0,398):
		  if ((output[i+1]-output[i])*(output[i+2]-output[i+1]))<=0:
		    directionchange+=1    
          
		if zeroCrossRE>0:
			DirChanzeroCross = directionchange/zeroCrossRE  # relation between direction change and Zero cross
		# calculate std
		stdRE = numpy.std(output)
		#calculate normalized spectral spectral
		FFT = numpy.fft.fft(output)
		specenergy= 0.0	 #Normalized spectral Energy
		Entropy= 0.0               	
		for i in range (0,400):
			Sum = FFT[i]*FFT[i]+ Sum
		avgFFT =FFT/400
		for i in range (0,400):		
		#	P[i]= (FFT[i]*FFT[i])/Sum
			if Sum>0:
              			specenergy= specenergy+ (FFT[i]*FFT[i]*FFT[i]*FFT[i])/(Sum*Sum)
		#calculate entropy
		#		Entropy= Entropy- ((FFT[i]*FFT[i])/Sum)*math.log((FFT[i]*FFT[i])/Sum, 2)
          	#count of signal peaks within 10% of the maximum
		tenPercentMaxRE = maxRE*0.9
		countRE=0.0
		for i in range(0,400):
			if output[i]>tenPercentMaxRE:
		    		countRE+=1
		avgzerocross = zeroCrossRE/400 # this feature is not important because related to zeroCross
		
		myFile = open("classification.tab", "w")
		myFile.write('mean\tmedian\tvar\tTCM\tRMS\tmax\tmin\tdiff\tcountmax10%\tdirectionchange\tEntropy\tSpecenergy\tzeroCross\tDirChanzeroCross\tavgzerocross\tavgFFT\tstddeviation\tlocation-coordinator\n') # Write a feature string to a tab file  #18 features
		myFile.write('c\tc\tc\tc\tc\tc\tc\tc\tc\tc\tc\tc\tc\tc\tc\tc\tc\td\n')  #18 
		myFile.write('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tclass\n')
		#myFile.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\t{12}\t{13}\t{14}\n'.format(meanRE, medianRE, varRE, TCM, rmsRE, maxRE, minRE, diffRE, countRE, directionchange, zeroCrossRE, DirChanzeroCross, avgzerocross, stdRE, coordinator))
		myFile.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\t{12}\t{13}\t{14}\t{15}\t{16}\n'.format(meanRE, medianRE, varRE, TCM, rmsRE, maxRE, minRE, diffRE, countRE, directionchange, specenergy, zeroCrossRE, DirChanzeroCross, avgzerocross, avgFFT, stdRE, coordinator))
		#myFile.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\n'.format(meanRE, medianRE, varRE, TCM, rmsRE, maxRE, minRE, diffRE, countRE, directionchange, Entropy, specenergy))							
		myFile.close()
		
		return self.variable_function_probe_1

class MainWindow(wx.Frame, top_block):
    def __init__(self, parent, title):
        self.dirname=''

        # A "-1" in the size parameter instructs wxWidgets to use the default size.
        # In this case, we select 200px width and the default height.
        wx.Frame.__init__(self, parent, title=title, size=(200,-1))
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar() # A Statusbar in the bottom of the window

        # Setting up the menu.
        filemenu= wx.Menu()
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open"," Open a file to edit")
        menuAbout= filemenu.Append(wx.ID_ABOUT, "&Start Recording"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&Action") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Events.
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.buttons = []
#        #for i in range(0, 6):
#            #self.buttons.append(wx.Button(self, -1, "Button &"+str(i)))
#            #self.sizer2.Add(self.buttons[i], 1, wx.EXPAND)
        self.buttons.append(wx.Button(self, -1, "Start Recording"))
        self.sizer2.Add(self.buttons[0], 1, wx.EXPAND)
        
        
        self.buttons.append(wx.Button(self, -1, "Stop"))
        self.sizer2.Add(self.buttons[1], 1, wx.EXPAND)
        
        self.buttons.append(wx.Button(self, -1, "Store"))
        self.sizer2.Add(self.buttons[2], 1, wx.EXPAND)
        
        self.buttons.append(wx.Button(self, -1, "Display"))
        self.sizer2.Add(self.buttons[3], 1, wx.EXPAND)
        
        
        
        # Use some sizers to see layout options
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.control, 1, wx.EXPAND)
        self.sizer.Add(self.sizer2, 0, wx.EXPAND)

        #Layout sizers
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        self.Show()
        
    def OnAbout(self,e):
        qapp = Qt.QApplication(sys.argv)
        tb = top_block()
        tb.start()
        tb.show()
        qapp.exec_()
        tb.stop()
        
        # Create a message dialog box
#        dlg = wx.MessageDialog(self, " Indoor Location  \n Write in Python and Orange", "Indoor Location Program", wx.OK)
#        dlg.ShowModal() # Shows it
#        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True)  # Close the frame.

    def OnOpen(self,e):
        """ Open a file"""
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'r')
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()
    def EvtRadioBox(self, event):
        self.logger.AppendText('EvtRadioBox: %d\n' % event.GetInt())
    def EvtComboBox(self, event):
        self.logger.AppendText('EvtComboBox: %s\n' % event.GetString())
    def OnClick(self,event):
        self.logger.AppendText(" Click on object with Id %d\n" %event.GetId())
    def EvtText(self, event):
        self.logger.AppendText('EvtText: %s\n' % event.GetString())
    def EvtChar(self, event):
        self.logger.AppendText('EvtChar: %d\n' % event.GetKeyCode())
        event.Skip()
    def EvtCheckBox(self, event):
        self.logger.AppendText('EvtCheckBox: %d\n' % event.Checked())

if __name__ == '__main__':
     coordinator = input("Enter testing coordinator Room, row, column:")
     parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
     (options, args) = parser.parse_args()
     app = wx.App(False)
     frame = MainWindow(None, "Indoor Location Learning")
     app.MainLoop()
#     qapp = Qt.QApplication(sys.argv)
#     tb = top_block()
#     tb.start()
#     tb.show()
#     qapp.exec_()
#     tb.stop()
