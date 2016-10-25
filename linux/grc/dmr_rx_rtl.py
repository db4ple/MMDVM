#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Dmr Rx Rtl
# Generated: Tue Oct 25 22:11:36 2016
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr
import time


class dmr_rx_rtl(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Dmr Rx Rtl")

        ##################################################
        # Variables
        ##################################################
        self.samp_rx_rf = samp_rx_rf = 1200000
        self.samp_rx_audio = samp_rx_audio = 24000
        
        self.rx_xlate_taps = rx_xlate_taps = firdes.low_pass(1.0, samp_rx_rf, 60000, 10000, firdes.WIN_HAMMING, 6.76)
          

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "rtl_sdr=0" )
        self.osmosdr_source_0.set_sample_rate(samp_rx_rf)
        self.osmosdr_source_0.set_center_freq(431.825e6, 0)
        self.osmosdr_source_0.set_freq_corr(139, 0)
        self.osmosdr_source_0.set_dc_offset_mode(2, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, (rx_xlate_taps), 50000, samp_rx_rf)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((1, ))
        self.blocks_float_to_short_0 = blocks.float_to_short(1, 200)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_short*1, "/opt/dmr/sampRX", False)
        self.blocks_file_sink_0.set_unbuffered(True)
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=samp_rx_audio,
        	quad_rate=samp_rx_rf,
        	tau=0.0001e-6,
        	max_dev=5e3,
          )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_nbfm_rx_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.blocks_float_to_short_0, 0), (self.blocks_file_sink_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_float_to_short_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_nbfm_rx_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))    

    def get_samp_rx_rf(self):
        return self.samp_rx_rf

    def set_samp_rx_rf(self, samp_rx_rf):
        self.samp_rx_rf = samp_rx_rf
        self.osmosdr_source_0.set_sample_rate(self.samp_rx_rf)

    def get_samp_rx_audio(self):
        return self.samp_rx_audio

    def set_samp_rx_audio(self, samp_rx_audio):
        self.samp_rx_audio = samp_rx_audio

    def get_rx_xlate_taps(self):
        return self.rx_xlate_taps

    def set_rx_xlate_taps(self, rx_xlate_taps):
        self.rx_xlate_taps = rx_xlate_taps
        self.freq_xlating_fir_filter_xxx_0.set_taps((self.rx_xlate_taps))


def main(top_block_cls=dmr_rx_rtl, options=None):

    tb = top_block_cls()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
