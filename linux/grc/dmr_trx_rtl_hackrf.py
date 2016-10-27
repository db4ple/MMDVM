#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Dmr Trx Rtl Hackrf
# Generated: Thu Oct 27 18:15:42 2016
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


class dmr_trx_rtl_hackrf(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Dmr Trx Rtl Hackrf")

        ##################################################
        # Variables
        ##################################################
        self.samp_rx_rf = samp_rx_rf = 1200000
        self.scale = scale = 8192.0
        self.samp_rx_audio = samp_rx_audio = 24000
        self.samp_rate = samp_rate = 24000
        
        self.rx_xlate_taps = rx_xlate_taps = firdes.low_pass(1.0, samp_rx_rf, 60000, 10000, firdes.WIN_HAMMING, 6.76)
          
        self.max_val = max_val = 881.0

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=int(8e6),
                decimation=samp_rate,
                taps=None,
                fractional_bw=None,
        )
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
          
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + "hackrf=000000000000000014d463dc2f162ee1" )
        self.osmosdr_sink_0.set_sample_rate(int(8e6))
        self.osmosdr_sink_0.set_center_freq(431.875e6, 0)
        self.osmosdr_sink_0.set_freq_corr(3.5, 0)
        self.osmosdr_sink_0.set_gain(10, 0)
        self.osmosdr_sink_0.set_if_gain(20, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna("", 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)
          
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, (rx_xlate_taps), 50000, samp_rx_rf)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(300, 600, 0)
        self.blocks_short_to_float_0_1_2 = blocks.short_to_float(1, 1)
        self.blocks_short_to_float_0 = blocks.short_to_float(1, -int(scale))
        self.blocks_multiply_xx_0 = blocks.multiply_vss(1)
        self.blocks_moving_average_xx_1 = blocks.moving_average_ff(24*30, 1.0/(30*24.0), 4000)
        self.blocks_float_to_short_1 = blocks.float_to_short(1, -1.0)
        self.blocks_float_to_short_0 = blocks.float_to_short(1, 200)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_short*1, "/opt/dmr/sampTX", False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_short*1, "/opt/dmr/sampRX", False)
        self.blocks_file_sink_0.set_unbuffered(True)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_short*1, 12000)
        self.blocks_add_const_vxx_0 = blocks.add_const_vss((1, ))
        self.blocks_abs_xx_0 = blocks.abs_ss()
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=samp_rx_audio,
        	quad_rate=samp_rx_rf,
        	tau=0.0001e-6,
        	max_dev=5e3,
          )
        self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc(6)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_frequency_modulator_fc_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.analog_nbfm_rx_0, 0), (self.blocks_float_to_short_0, 0))    
        self.connect((self.blocks_abs_xx_0, 0), (self.blocks_delay_0, 0))    
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_multiply_xx_0, 0))    
        self.connect((self.blocks_delay_0, 0), (self.blocks_short_to_float_0_1_2, 0))    
        self.connect((self.blocks_file_source_0, 0), (self.blocks_abs_xx_0, 0))    
        self.connect((self.blocks_file_source_0, 0), (self.blocks_short_to_float_0, 0))    
        self.connect((self.blocks_float_to_short_0, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.blocks_float_to_short_1, 0), (self.blocks_add_const_vxx_0, 0))    
        self.connect((self.blocks_moving_average_xx_1, 0), (self.blocks_threshold_ff_0, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_file_sink_0, 0))    
        self.connect((self.blocks_short_to_float_0, 0), (self.analog_frequency_modulator_fc_0, 0))    
        self.connect((self.blocks_short_to_float_0_1_2, 0), (self.blocks_moving_average_xx_1, 0))    
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_float_to_short_1, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_nbfm_rx_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.osmosdr_sink_0, 0))    

    def get_samp_rx_rf(self):
        return self.samp_rx_rf

    def set_samp_rx_rf(self, samp_rx_rf):
        self.samp_rx_rf = samp_rx_rf
        self.osmosdr_source_0.set_sample_rate(self.samp_rx_rf)

    def get_scale(self):
        return self.scale

    def set_scale(self, scale):
        self.scale = scale
        self.blocks_short_to_float_0.set_scale(-int(self.scale))

    def get_samp_rx_audio(self):
        return self.samp_rx_audio

    def set_samp_rx_audio(self, samp_rx_audio):
        self.samp_rx_audio = samp_rx_audio

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_rx_xlate_taps(self):
        return self.rx_xlate_taps

    def set_rx_xlate_taps(self, rx_xlate_taps):
        self.rx_xlate_taps = rx_xlate_taps
        self.freq_xlating_fir_filter_xxx_0.set_taps((self.rx_xlate_taps))

    def get_max_val(self):
        return self.max_val

    def set_max_val(self, max_val):
        self.max_val = max_val


def main(top_block_cls=dmr_trx_rtl_hackrf, options=None):

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
