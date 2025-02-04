#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Jammer Gen
# GNU Radio version: 3.10.11.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from xmlrpc.server import SimpleXMLRPCServer
import threading
import osmosdr
import time
import sip



class jammer_gen(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Jammer Gen", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Jammer Gen")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "jammer_gen")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.var_rf_gain = var_rf_gain = 0
        self.var_if_gain = var_if_gain = 60
        self.var_cent_freq = var_cent_freq = 446000000
        self.var_bb_gain = var_bb_gain = 60
        self.var_bandwidth = var_bandwidth = 20e6
        self.samp_rate = samp_rate = 2e6
        self.sample_rate = sample_rate = samp_rate
        self.rf_gain = rf_gain = var_rf_gain
        self.if_gain = if_gain = var_if_gain
        self.cent_freq = cent_freq = var_cent_freq
        self.bb_gain = bb_gain = var_bb_gain
        self.bandwidth = bandwidth = var_bandwidth

        ##################################################
        # Blocks
        ##################################################

        self._sample_rate_range = qtgui.Range(1e6, 20e6, 10, samp_rate, 200)
        self._sample_rate_win = qtgui.RangeWidget(self._sample_rate_range, self.set_sample_rate, "Sample rate", "slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._sample_rate_win)
        self._rf_gain_range = qtgui.Range(10, 60, 10, var_rf_gain, 200)
        self._rf_gain_win = qtgui.RangeWidget(self._rf_gain_range, self.set_rf_gain, "RF gain", "slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._rf_gain_win)
        self._if_gain_range = qtgui.Range(10, 60, 10, var_if_gain, 200)
        self._if_gain_win = qtgui.RangeWidget(self._if_gain_range, self.set_if_gain, "IF gain", "slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._if_gain_win)
        self._cent_freq_range = qtgui.Range(10e6, 6000e6, 500, var_cent_freq, 200)
        self._cent_freq_win = qtgui.RangeWidget(self._cent_freq_range, self.set_cent_freq, "Freq", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._cent_freq_win)
        self._bb_gain_range = qtgui.Range(10, 60, 10, var_bb_gain, 200)
        self._bb_gain_win = qtgui.RangeWidget(self._bb_gain_range, self.set_bb_gain, "BB gain", "slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._bb_gain_win)
        self._bandwidth_range = qtgui.Range(2e6, 50e6, 10, var_bandwidth, 200)
        self._bandwidth_win = qtgui.RangeWidget(self._bandwidth_range, self.set_bandwidth, "Bandwidth", "slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._bandwidth_win)
        self.xmlrpc_server_0 = SimpleXMLRPCServer(('localhost', 8888), allow_none=True)
        self.xmlrpc_server_0.register_instance(self)
        self.xmlrpc_server_0_thread = threading.Thread(target=self.xmlrpc_server_0.serve_forever)
        self.xmlrpc_server_0_thread.daemon = True
        self.xmlrpc_server_0_thread.start()
        self.qtgui_sink_x_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            cent_freq, #fc
            bandwidth, #bw
            "", #name
            True, #plotfreq
            False, #plotwaterfall
            False, #plottime
            False, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(True)

        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        self.osmosdr_sink_0 = osmosdr.sink(
            args="numchan=" + str(1) + " " + ''
        )
        self.osmosdr_sink_0.set_time_now(osmosdr.time_spec_t(time.time()), osmosdr.ALL_MBOARDS)
        self.osmosdr_sink_0.set_sample_rate(sample_rate)
        self.osmosdr_sink_0.set_center_freq(cent_freq, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(rf_gain, 0)
        self.osmosdr_sink_0.set_if_gain(if_gain, 0)
        self.osmosdr_sink_0.set_bb_gain(bb_gain, 0)
        self.osmosdr_sink_0.set_antenna('1', 0)
        self.osmosdr_sink_0.set_bandwidth(bandwidth, 0)
        self.analog_noise_source_x_1 = analog.noise_source_c(analog.GR_GAUSSIAN, 100, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_1, 0), (self.osmosdr_sink_0, 0))
        self.connect((self.analog_noise_source_x_1, 0), (self.qtgui_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "jammer_gen")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_var_rf_gain(self):
        return self.var_rf_gain

    def set_var_rf_gain(self, var_rf_gain):
        self.var_rf_gain = var_rf_gain
        self.set_rf_gain(self.var_rf_gain)

    def get_var_if_gain(self):
        return self.var_if_gain

    def set_var_if_gain(self, var_if_gain):
        self.var_if_gain = var_if_gain
        self.set_if_gain(self.var_if_gain)

    def get_var_cent_freq(self):
        return self.var_cent_freq

    def set_var_cent_freq(self, var_cent_freq):
        self.var_cent_freq = var_cent_freq
        self.set_cent_freq(self.var_cent_freq)

    def get_var_bb_gain(self):
        return self.var_bb_gain

    def set_var_bb_gain(self, var_bb_gain):
        self.var_bb_gain = var_bb_gain
        self.set_bb_gain(self.var_bb_gain)

    def get_var_bandwidth(self):
        return self.var_bandwidth

    def set_var_bandwidth(self, var_bandwidth):
        self.var_bandwidth = var_bandwidth
        self.set_bandwidth(self.var_bandwidth)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_sample_rate(self.samp_rate)

    def get_sample_rate(self):
        return self.sample_rate

    def set_sample_rate(self, sample_rate):
        self.sample_rate = sample_rate
        self.osmosdr_sink_0.set_sample_rate(self.sample_rate)

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.osmosdr_sink_0.set_gain(self.rf_gain, 0)

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain
        self.osmosdr_sink_0.set_if_gain(self.if_gain, 0)

    def get_cent_freq(self):
        return self.cent_freq

    def set_cent_freq(self, cent_freq):
        self.cent_freq = cent_freq
        self.osmosdr_sink_0.set_center_freq(self.cent_freq, 0)
        self.qtgui_sink_x_0.set_frequency_range(self.cent_freq, self.bandwidth)

    def get_bb_gain(self):
        return self.bb_gain

    def set_bb_gain(self, bb_gain):
        self.bb_gain = bb_gain
        self.osmosdr_sink_0.set_bb_gain(self.bb_gain, 0)

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self.osmosdr_sink_0.set_bandwidth(self.bandwidth, 0)
        self.qtgui_sink_x_0.set_frequency_range(self.cent_freq, self.bandwidth)




def main(top_block_cls=jammer_gen, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
