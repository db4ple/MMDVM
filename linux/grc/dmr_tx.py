#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Mon Oct 24 20:58:07 2016
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


class top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")

        ##################################################
        # Variables
        ##################################################
        self.scale = scale = 8192.0
        self.samp_rate = samp_rate = 24000
        self.max_val = max_val = 881.0

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=int(2e6),
                decimation=samp_rate,
                taps=None,
                fractional_bw=None,
        )
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + "hackrf=000000000000000014d463dc2f162ee1" )
        self.osmosdr_sink_0.set_sample_rate(int(2e6))
        self.osmosdr_sink_0.set_center_freq(431.875e6, 0)
        self.osmosdr_sink_0.set_freq_corr(3.5, 0)
        self.osmosdr_sink_0.set_gain(10, 0)
        self.osmosdr_sink_0.set_if_gain(20, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna("", 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)
          
        self.blocks_short_to_float_0 = blocks.short_to_float(1, -int(scale))
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_short*1, "/opt/dmr/sampTX", False)
        self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc(8)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_frequency_modulator_fc_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.blocks_file_source_0, 0), (self.blocks_short_to_float_0, 0))    
        self.connect((self.blocks_short_to_float_0, 0), (self.analog_frequency_modulator_fc_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.osmosdr_sink_0, 0))    

    def get_scale(self):
        return self.scale

    def set_scale(self, scale):
        self.scale = scale
        self.blocks_short_to_float_0.set_scale(-int(self.scale))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_max_val(self):
        return self.max_val

    def set_max_val(self, max_val):
        self.max_val = max_val


def main(top_block_cls=top_block, options=None):

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
