#!/usr/bin/env python2

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
import wx


if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"


class am_receive(grc_wxgui.top_block_gui):

    def __init__(self, file_path, min_freq, max_freq, min_volume, max_volume, default_samp_rate,default_resamp_factor, cutoff_freq):
        grc_wxgui.top_block_gui.__init__(self, title="Am Receive")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        # Variables

        self.volume = volume = 0.05
        self.samp_rate = samp_rate = default_samp_rate
        self.resamp_factor = resamp_factor = default_resamp_factor
        self.freq = freq = 0

        # Blocks

        # Volume Slider
        _volume_sizer = wx.BoxSizer(wx.VERTICAL)
        self._volume_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_volume_sizer,
        	value=self.volume,
        	callback=self.set_volume,
        	label='volume',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._volume_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_volume_sizer,
        	value=self.volume,
        	callback=self.set_volume,
        	minimum=min_volume,
        	maximum=max_volume,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_volume_sizer)

        # Frequency Slider
        _freq_sizer = wx.BoxSizer(wx.VERTICAL)
        self._freq_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_freq_sizer,
        	value=self.freq,
        	callback=self.set_freq,
        	label='freq',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._freq_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_freq_sizer,
        	value=self.freq,
        	callback=self.set_freq,
        	minimum=min_freq,
        	maximum=max_freq,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_freq_sizer)

        # Source GUI
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="Source FFT Plot",
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0.win)

        # Sink GUI
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_f(
        	self.GetWin(),
        	title="Scope Plot",
        	sample_rate=samp_rate/resamp_factor,
        	v_scale=0,
        	v_offset=0,
        	t_scale=0,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label="Counts",
        )
        self.Add(self.wxgui_scopesink2_0.win)

        # Sampler before sink
        self.rational_resampler_xxx_1 = filter.rational_resampler_fff(
                interpolation=1,
                decimation=4,
                taps=None,
                fractional_bw=None,
        )

        # Sampler after source
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=48000/((samp_rate/resamp_factor)/resamp_factor),
                decimation=resamp_factor,
                taps=None,
                fractional_bw=None,
        )

        # Low Pass Filter
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate/resamp_factor, cutoff_freq, 100, firdes.WIN_HAMMING, 6.76))

        # Mulitply Source with Cosine Wave
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)

        # Multiply volume with constant (Slider)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((volume, ))

        # File Source
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, file_path, True)

        # Complex to Magnitude Converter
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)

        # Audio Sink
        self.audio_sink_0 = audio.sink(48000, "", True)

        # Wave generator
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, freq, 1, 0)

        # Automatic Volume Adjustment
        self.analog_agc2_xx_0 = analog.agc2_cc(6.25e-4, 1e-5, 1.0, 1.0)
        self.analog_agc2_xx_0.set_max_gain(65536)


        # Connections

        self.connect((self.analog_agc2_xx_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.wxgui_fftsink2_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_agc2_xx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.audio_sink_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.wxgui_scopesink2_0, 0))

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self._volume_slider.set_value(self.volume)
        self._volume_text_box.set_value(self.volume)
        self.blocks_multiply_const_vxx_0.set_k((self.volume, ))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate/self.resamp_factor, cutoff_freq, 100, firdes.WIN_HAMMING, 6.76))
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.wxgui_scopesink2_0.set_sample_rate(self.samp_rate/self.resamp_factor)

    def get_resamp_factor(self):
        return self.resamp_factor

    def set_resamp_factor(self, resamp_factor):
        self.resamp_factor = resamp_factor
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate/self.resamp_factor, cutoff_freq, 100, firdes.WIN_HAMMING, 6.76))
        self.wxgui_scopesink2_0.set_sample_rate(self.samp_rate/self.resamp_factor)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self._freq_slider.set_value(self.freq)
        self._freq_text_box.set_value(self.freq)
        self.analog_sig_source_x_0.set_frequency(self.freq)


def main(file_path, min_freq, max_freq, min_volume, max_volume, default_samp_rate,default_resamp_factor, cutoff_freq):

    tb = am_receive(file_path, min_freq, max_freq, min_volume, max_volume, default_samp_rate,default_resamp_factor, cutoff_freq)
    tb.Start(True)
    tb.Wait()

# Variables

file_path = "/home/nowismytime/Downloads/am_usrp710.dat"

# variables for frequency slider
min_freq = -127000
max_freq = 127000

# variables for volume slider
min_volume = 0
max_volume = 1

default_samp_rate = 256000
default_resamp_factor = 4
cutoff_freq = 5000

wave_type = "cos"



if __name__ == '__main__':
    main(file_path, min_freq, max_freq, min_volume, max_volume, default_samp_rate,default_resamp_factor, cutoff_freq)