#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Dmr Trx Rtl Hackrf
# Generated: Mon Oct 31 09:50:10 2016
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import math
import osmosdr
import time


class dmr_trx_rtl_hackrf(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Dmr Trx Rtl Hackrf")

        ##################################################
        # Variables
        ##################################################
        self.samp_rx_rf = samp_rx_rf = 240000
        self.scale = scale = 8192.0
        self.samp_rx_audio = samp_rx_audio = 24000
        self.samp_rate = samp_rate = 24000
        
        self.rx_xlate_taps = rx_xlate_taps = firdes.low_pass(1.0, samp_rx_rf, 12500, 2000, firdes.WIN_HAMMING, 6.76)
          
        self.rx_dev = rx_dev = 50000
        self.rx_dec = rx_dec = 1
        self.max_val = max_val = 881.0
        self.fsk_deviation_hz = fsk_deviation_hz = 5000
        self.config_ppm_rtl = config_ppm_rtl = 0 
        self.config_ppm_hrf = config_ppm_hrf = 3.5
        self.config_freq = config_freq = 434.787500e6
        self.config_delay = config_delay = 0 

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_1 = filter.rational_resampler_fff(
                interpolation=1,
                decimation=samp_rx_rf/rx_dec/samp_rx_audio,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=int(2e6),
                decimation=samp_rate,
                taps=None,
                fractional_bw=None,
        )
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "rtl_sdr=0,buflen=512,buffers=4" )
        self.osmosdr_source_0.set_sample_rate(samp_rx_rf)
        self.osmosdr_source_0.set_center_freq(config_freq-rx_dev, 0)
        self.osmosdr_source_0.set_freq_corr(config_ppm_rtl, 0)
        self.osmosdr_source_0.set_dc_offset_mode(2, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + "hackrf=e1,buffers=2" )
        self.osmosdr_sink_0.set_sample_rate(int(2e6))
        self.osmosdr_sink_0.set_center_freq(config_freq, 0)
        self.osmosdr_sink_0.set_freq_corr(config_ppm_hrf, 0)
        self.osmosdr_sink_0.set_gain(0, 0)
        self.osmosdr_sink_0.set_if_gain(0, 0)
        self.osmosdr_sink_0.set_bb_gain(50, 0)
        self.osmosdr_sink_0.set_antenna("", 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)
          
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(rx_dec, (rx_xlate_taps), rx_dev, samp_rx_rf)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(10, 40, 0)
        self.blocks_short_to_float_0_1_2 = blocks.short_to_float(1, 1)
        self.blocks_short_to_float_0 = blocks.short_to_float(1, -int(scale))
        self.blocks_multiply_xx_0 = blocks.multiply_vss(1)
        self.blocks_moving_average_xx_1 = blocks.moving_average_ff(24*30, 1.0/(30*24.0), 4000)
        self.blocks_float_to_short_1 = blocks.float_to_short(1, -1.0)
        self.blocks_float_to_short_0 = blocks.float_to_short(1, 300)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_short*1, "/opt/dmr/sampTX", False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_short*1, "/opt/dmr/sampRX", False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_short*1, config_delay)
        self.blocks_add_const_vxx_0 = blocks.add_const_vss((1, ))
        self.blocks_abs_xx_0 = blocks.abs_ss()
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf((samp_rx_rf/rx_dec)/(2*math.pi*fsk_deviation_hz/8.0))
        self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc(7)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_frequency_modulator_fc_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.rational_resampler_xxx_1, 0))    
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
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_quadrature_demod_cf_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.osmosdr_sink_0, 0))    
        self.connect((self.rational_resampler_xxx_1, 0), (self.blocks_float_to_short_0, 0))    

    def get_samp_rx_rf(self):
        return self.samp_rx_rf

    def set_samp_rx_rf(self, samp_rx_rf):
        self.samp_rx_rf = samp_rx_rf
        self.analog_quadrature_demod_cf_0.set_gain((self.samp_rx_rf/self.rx_dec)/(2*math.pi*self.fsk_deviation_hz/8.0))
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

    def get_rx_dev(self):
        return self.rx_dev

    def set_rx_dev(self, rx_dev):
        self.rx_dev = rx_dev
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.rx_dev)
        self.osmosdr_source_0.set_center_freq(self.config_freq-self.rx_dev, 0)

    def get_rx_dec(self):
        return self.rx_dec

    def set_rx_dec(self, rx_dec):
        self.rx_dec = rx_dec
        self.analog_quadrature_demod_cf_0.set_gain((self.samp_rx_rf/self.rx_dec)/(2*math.pi*self.fsk_deviation_hz/8.0))

    def get_max_val(self):
        return self.max_val

    def set_max_val(self, max_val):
        self.max_val = max_val

    def get_fsk_deviation_hz(self):
        return self.fsk_deviation_hz

    def set_fsk_deviation_hz(self, fsk_deviation_hz):
        self.fsk_deviation_hz = fsk_deviation_hz
        self.analog_quadrature_demod_cf_0.set_gain((self.samp_rx_rf/self.rx_dec)/(2*math.pi*self.fsk_deviation_hz/8.0))

    def get_config_ppm_rtl(self):
        return self.config_ppm_rtl

    def set_config_ppm_rtl(self, config_ppm_rtl):
        self.config_ppm_rtl = config_ppm_rtl
        self.osmosdr_source_0.set_freq_corr(self.config_ppm_rtl, 0)

    def get_config_ppm_hrf(self):
        return self.config_ppm_hrf

    def set_config_ppm_hrf(self, config_ppm_hrf):
        self.config_ppm_hrf = config_ppm_hrf
        self.osmosdr_sink_0.set_freq_corr(self.config_ppm_hrf, 0)

    def get_config_freq(self):
        return self.config_freq

    def set_config_freq(self, config_freq):
        self.config_freq = config_freq
        self.osmosdr_source_0.set_center_freq(self.config_freq-self.rx_dev, 0)
        self.osmosdr_sink_0.set_center_freq(self.config_freq, 0)

    def get_config_delay(self):
        return self.config_delay

    def set_config_delay(self, config_delay):
        self.config_delay = config_delay
        self.blocks_delay_0.set_dly(self.config_delay)


def main(top_block_cls=dmr_trx_rtl_hackrf, options=None):

    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    tb = top_block_cls()
    tb.start(1000)
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
