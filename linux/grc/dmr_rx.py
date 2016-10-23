#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Sun Oct 23 18:48:03 2016
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import time
import wx


class top_block(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Top Block")

        ##################################################
        # Variables
        ##################################################
        self.samp_rx_rf = samp_rx_rf = 1200000
        self.sens = sens = 295.74
        self.samp_rx_audio = samp_rx_audio = 24000
        self.samp_rate = samp_rate = 48000
        
        self.rx_xlate_taps = rx_xlate_taps = firdes.low_pass(1.0, samp_rx_rf, 60000, 10000, firdes.WIN_HAMMING, 6.76)
          

        ##################################################
        # Blocks
        ##################################################
        self.wxgui_scopesink2_0_0 = scopesink2.scope_sink_f(
        	self.GetWin(),
        	title="Scope Plot",
        	sample_rate=samp_rx_audio,
        	v_scale=0,
        	v_offset=0,
        	t_scale=0,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_FREE,
        	y_axis_label="Counts",
        )
        self.Add(self.wxgui_scopesink2_0_0.win)
        self.wxgui_fftsink2_0_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rx_audio,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="FFT Plot",
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0_0.win)
        _sens_sizer = wx.BoxSizer(wx.VERTICAL)
        self._sens_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_sens_sizer,
        	value=self.sens,
        	callback=self.set_sens,
        	label='sens',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._sens_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_sens_sizer,
        	value=self.sens,
        	callback=self.set_sens,
        	minimum=200,
        	maximum=600,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_sens_sizer)
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccc(
                interpolation=samp_rx_audio,
                decimation=samp_rx_rf,
                taps=None,
                fractional_bw=None,
        )
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "rtl_sdr=0" )
        self.osmosdr_source_0.set_sample_rate(samp_rx_rf)
        self.osmosdr_source_0.set_center_freq(431.825e6, 0)
        self.osmosdr_source_0.set_freq_corr(138, 0)
        self.osmosdr_source_0.set_dc_offset_mode(2, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rx_audio, 6000, 1000, firdes.WIN_HAMMING, 6.76))
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, (rx_xlate_taps), 50000, samp_rx_rf)
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink("/tmp/sampRX", 1, samp_rx_audio, 16)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((-0.05, ))
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
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_wavfile_sink_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.wxgui_scopesink2_0_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_nbfm_rx_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.rational_resampler_xxx_0_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.wxgui_fftsink2_0_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))    
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.low_pass_filter_0, 0))    

    def get_samp_rx_rf(self):
        return self.samp_rx_rf

    def set_samp_rx_rf(self, samp_rx_rf):
        self.samp_rx_rf = samp_rx_rf
        self.osmosdr_source_0.set_sample_rate(self.samp_rx_rf)

    def get_sens(self):
        return self.sens

    def set_sens(self, sens):
        self.sens = sens
        self._sens_slider.set_value(self.sens)
        self._sens_text_box.set_value(self.sens)

    def get_samp_rx_audio(self):
        return self.samp_rx_audio

    def set_samp_rx_audio(self, samp_rx_audio):
        self.samp_rx_audio = samp_rx_audio
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rx_audio, 6000, 1000, firdes.WIN_HAMMING, 6.76))
        self.wxgui_fftsink2_0_0.set_sample_rate(self.samp_rx_audio)
        self.wxgui_scopesink2_0_0.set_sample_rate(self.samp_rx_audio)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_rx_xlate_taps(self):
        return self.rx_xlate_taps

    def set_rx_xlate_taps(self, rx_xlate_taps):
        self.rx_xlate_taps = rx_xlate_taps
        self.freq_xlating_fir_filter_xxx_0.set_taps((self.rx_xlate_taps))


def main(top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()



if __name__ == '__main__':
    main()
