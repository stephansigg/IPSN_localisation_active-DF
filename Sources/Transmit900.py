#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Transmit900
# Generated: Thu Dec 12 12:06:19 2013
##################################################

from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import time
import wx

class transmit900(grc_wxgui.top_block_gui):

	def __init__(self):
		grc_wxgui.top_block_gui.__init__(self, title="Transmit900")

		##################################################
		# Variables
		##################################################
		self.samp_rate = samp_rate = 320000

		##################################################
		# Blocks
		##################################################
		self.uhd_usrp_sink_0 = uhd.usrp_sink(
			device_addr="",
			stream_args=uhd.stream_args(
				cpu_format="fc32",
				channels=range(1),
			),
		)
		self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
		self.uhd_usrp_sink_0.set_center_freq(900000000, 0)
		self.uhd_usrp_sink_0.set_gain(30, 0)
		self.gr_sig_source_x_0 = gr.sig_source_c(samp_rate, gr.GR_SIN_WAVE, 1000, 1, 0)
		self.gr_multiply_const_vxx_0 = gr.multiply_const_vcc((16384, ))

		##################################################
		# Connections
		##################################################
		self.connect((self.gr_sig_source_x_0, 0), (self.gr_multiply_const_vxx_0, 0))
		self.connect((self.gr_multiply_const_vxx_0, 0), (self.uhd_usrp_sink_0, 0))


	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.gr_sig_source_x_0.set_sampling_freq(self.samp_rate)
		self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	tb = transmit900()
	tb.Run(True)
