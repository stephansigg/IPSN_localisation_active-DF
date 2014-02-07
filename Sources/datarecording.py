#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: writeToFile
# Author: stephan sigg
# Description: USRP source write to file
# Generated: Mon May 27 12:41:33 2013
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
import testorange

###################################
### Orange:
#import orange, orngTree
######################
# import for svm:
#from Orange.classification import svm
#from Orange.evaluation import testing, scoring
######################
# For Confusion matrix:
#import orngTest, orngStat
######################
#import Orange
##############################
### for the queue
from collections import deque
import collections
import numpy
#import testorange # call classification function
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
         
#         # initialise classifiers
#		self.train_data = orange.ExampleTable("classification.tab")
#		#bayes = orange.BayesLearner(train_data)
#		#tree = orngTree.TreeLearner(train_data)
#		self.knnLearner = orange.kNNLearner(self.train_data)
#		#svm = svm.SVMLearner(train_data)
#		#bayes.name = "bayes"
#		#tree.name = "tree"
#		self.knnLearner.name = "knn"
#		#svm.name = "svm"
#		self.knnLearner.k = 10
		

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
#			myFile = open("classification.tab", "a")
#			myFile.write('mean\tmedian\tvar\tTCM\tRMS\tmax\tmin\tdiff\tcountmax10%\tdirectionchange\tzeroCross\tDirChanzeroCross\tavgzerocross\tstddeviation\tlocation-coordinator\n')
#			#myFile.write('mean\tmedian\tvar\tTCM\tRMS\tmax\tmin\tdiff\tcountmax10%\tdirectionchange\tEntropy\tSpecenergy\tzeroCross\tDirChanzeroCross\tavgzerocross\tavgFFT\tstddeviation\tlocation-coordinator\n') # Write a feature string to a tab file  #18 features
#			myFile.write('c\tc\tc\tc\tc\tc\tc\tc\tc\tc\tc\tc\tc\tc\td\n')  #18 
#			myFile.write('\t\t\t\t\t\t\t\t\t\t\t\t\t\tclass\n')
#			myFile.close()
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
		myFile = open("classification.tab", "a")
		myFile.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\t{12}\t{13}\t{14}\n'.format(meanRE, medianRE, varRE, TCM, rmsRE, maxRE, minRE, diffRE, countRE, directionchange, zeroCrossRE, DirChanzeroCross, avgzerocross, stdRE, coordinator))							
         #myFile.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\t{12}\t{13}\t{14}\t{15}\t{16}\n'.format(meanRE, medianRE, varRE, TCM, rmsRE, maxRE, minRE, diffRE, countRE, directionchange, specenergy, zeroCrossRE, DirChanzeroCross, avgzerocross, avgFFT, stdRE, coordinator))							
				
         	myFile.close()
		return self.variable_function_probe_1

class top_block1(gr.top_block, Qt.QWidget): #store test file
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
         
#         # initialise classifiers
#		self.train_data = orange.ExampleTable("classification.tab")
#		#bayes = orange.BayesLearner(train_data)
#		#tree = orngTree.TreeLearner(train_data)
#		self.knnLearner = orange.kNNLearner(self.train_data)
#		#svm = svm.SVMLearner(train_data)
#		#bayes.name = "bayes"
#		#tree.name = "tree"
#		self.knnLearner.name = "knn"
#		#svm.name = "svm"
#		self.knnLearner.k = 10
		

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
#			myFile = open("testing.tab", "a")
#			myFile.write('mean\tmedian\tvar\tTCM\tRMS\tmax\tmin\tdiff\tcountmax10%\tdirectionchange\tzeroCross\tDirChanzeroCross\tavgzerocross\tstddeviation\tlocation-coordinator\n')
#			#myFile.write('mean\tmedian\tvar\tTCM\tRMS\tmax\tmin\tdiff\tcountmax10%\tdirectionchange\tEntropy\tSpecenergy\tzeroCross\tDirChanzeroCross\tavgzerocross\tavgFFT\tstddeviation\tlocation-coordinator\n') # Write a feature string to a tab file  #18 features
#			myFile.write('c\tc\tc\tc\tc\tc\tc\tc\tc\tc\tc\tc\tc\tc\td\n')  #18 
#			myFile.write('\t\t\t\t\t\t\t\t\t\t\t\t\t\tclass\n')
#			myFile.close()
			while True:
				# TODO: do classification here
				classification = self.get_classification()
				# TODO: Write out classification
				time.sleep(1.0/(20)) # One classification every 0.5 seconds
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
		coordinator1=2
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
		myFile = open("testing.tab", "a+")
  
		myFile.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\t{12}\t{13}\t{14}\n'.format(meanRE, medianRE, varRE, TCM, rmsRE, maxRE, minRE, diffRE, countRE, directionchange, zeroCrossRE, DirChanzeroCross, avgzerocross, stdRE, coordinator1))							
         #myFile.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\t{12}\t{13}\t{14}\t{15}\t{16}\n'.format(meanRE, medianRE, varRE, TCM, rmsRE, maxRE, minRE, diffRE, countRE, directionchange, specenergy, zeroCrossRE, DirChanzeroCross, avgzerocross, avgFFT, stdRE, coordinator))							
				
         	myFile.close()
		return self.variable_function_probe_1


class MainWindow(wx.Frame, top_block):
    def __init__(self, parent, title):
        self.dirname=''
        wx.Frame.__init__(self, parent, title=title, size=(200,-1))
        #self.quote = wx.StaticText(self, label="Your quote :", pos=(20, 30))

        # A multiline TextCtrl - This is here to show how the events work in this program, don't pay too much attention to it
        # use to export the final results
        self.logger1 = wx.TextCtrl(self, pos=(400,20), size=(200,500), style=wx.TE_MULTILINE | wx.TE_READONLY)
        # use to calculate Evaluating
        self.logger2 = wx.TextCtrl(self, pos=(650,20), size=(400,500), style=wx.TE_MULTILINE | wx.TE_READONLY)
        #confusion matrix         
        self.logger3 = wx.TextCtrl(self, pos=(1100,20), size=(400,500), style=wx.TE_MULTILINE | wx.TE_READONLY)
        # button function
        self.button1 =wx.Button(self, label="Start Recording", pos=(50, 150))
        self.Bind(wx.EVT_BUTTON, self.Start_record,self.button1)
        
        self.button2 =wx.Button(self, label="Testing& Evaluating", pos=(190, 150))
        self.Bind(wx.EVT_BUTTON, self.evaluating,self.button2)
        
        
        
        self.button3 =wx.Button(self, label="Accuracy & Confusion Matrix", pos=(190, 200))
        self.Bind(wx.EVT_BUTTON, self.evaluating1,self.button3)
        
    
        self.button4 =wx.Button(self, label="Classifying ", pos=(50, 200))
        self.Bind(wx.EVT_BUTTON, self.orange_classification, self.button4)
        
        self.button5 =wx.Button(self, label="Start Record Testing ", pos=(50, 250))
        self.Bind(wx.EVT_BUTTON, self.Start_record_testing,self.button5)
        
        
#        self.Bind(wx.EVT_BUTTON, self.OnClick2,self.button)
#        
#        self.button =wx.Button(self, label="Pause", pos=(350, 100))
#        self.Bind(wx.EVT_BUTTON, self.OnClick3,self.button)

        # the edit control - one line version.
        self.lblname = wx.StaticText(self, label="Coordinator :", pos=(20,60))
        self.editname = wx.TextCtrl(self, value="Enter Room", pos=(120, 60), size=(200,-1))
        
#        self.editname = wx.TextCtrl(self, value="Enter Row", pos=(270, 90), size=(200,-1))
#        self.lblname = wx.StaticText(self, label="Coordinator Row :", pos=(20,90))
#         
#        
#        self.lblname = wx.StaticText(self, label="Coordinator Column :", pos=(20,120))
#        self.editname = wx.TextCtrl(self, value="Enter Column", pos=(270, 120), size=(200,-1))   
        
        self.Bind(wx.EVT_TEXT, self.EvtText, self.editname)
        self.Bind(wx.EVT_CHAR, self.EvtChar, self.editname)
    #def Start_record_testing(self, event):
        
    def Start_record(self,event):
        qapp = Qt.QApplication(sys.argv)
        tb = top_block()
        tb.start()
        tb.show()
        qapp.exec_()
       # tb.stop()
    def Start_record_testing(self, event):
        qapp = Qt.QApplication(sys.argv)
        tb = top_block1()  #duplicate class top_block, only filename changed
        tb.start()
        tb.show()
        qapp.exec_()
        
    def Stop_record(self, event):
        tb = top_block()
        tb.stop()
    def orange_classification(self, event): # classification
                #print "location predicted", testorange.classification()
        self.logger1.AppendText('Location Predicted: %s\n' % testorange.classification())
    def evaluating(self, event):
        self.logger2.AppendText('Learner  CA     IS     Brier    AUC:\n %s\n' % testorange.evaluating())
    def evaluating1(self, event):
        self.logger3.AppendText('Accuracy bayes, tree, kNN %s\n' % testorange.accuracy())
        
    def EvtText(self, event):
        global coordinator
        coordinator = event.GetString()
    def EvtChar(self, event):
        self.logger.AppendText('EvtChar: %d\n' % event.GetKeyCode())
        event.Skip()
    def EvtCheckBox(self, event):
        self.logger.AppendText('EvtCheckBox: %d\n' % event.Checked())
#class Classification(MainWindow, top_block):
#    def 
    
if __name__ == '__main__':

     parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
     (options, args) = parser.parse_args()
     app = wx.App(False)
     frame = MainWindow(None, "Indoor Location Learning")
     frame.Show()
     app.MainLoop()
#     qapp = Qt.QApplication(sys.argv)
#     tb = top_block()
#     tb.start()
#     tb.show()
#     qapp.exec_()
#     tb.stop()
