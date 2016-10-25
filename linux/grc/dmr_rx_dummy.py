#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Tue Oct 25 19:36:13 2016
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser


class top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")

        ##################################################
        # Variables
        ##################################################
        self.samp_rx_audio = samp_rx_audio = 24000

        ##################################################
        # Blocks
        ##################################################
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_short*1, samp_rx_audio,True)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_short*1, "/opt/dmr/sampRX", True)
        self.blocks_file_sink_0.set_unbuffered(True)
        self.analog_const_source_x_0 = analog.sig_source_s(0, analog.GR_CONST_WAVE, 0, 0, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.blocks_file_sink_0, 0))    

    def get_samp_rx_audio(self):
        return self.samp_rx_audio

    def set_samp_rx_audio(self, samp_rx_audio):
        self.samp_rx_audio = samp_rx_audio
        self.blocks_throttle_0.set_sample_rate(self.samp_rx_audio)


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
