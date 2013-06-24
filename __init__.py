#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

'''
Gauge
=====

The :class:`Gauge` widget is a widget for displaying gauge. 

.. note::

Source svg file provided for customing.

'''

__all__ = ('Gauge')

__title__ = 'garden.gauge'
__version__ = '0.1'
__author__ = 'julien@hautefeuille.eu'

import kivy
kivy.require('1.7.1')
from kivy.config import Config
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.properties import BoundedNumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar

class Gauge(Widget):
    '''
    Gauge class

    '''

    unit = NumericProperty(1.8)
    value = BoundedNumericProperty(0, min=0, max=100, errorvalue=0)
    file_gauge = StringProperty("cadran.png")
    file_needle = StringProperty("needle.png")
    size_gauge = BoundedNumericProperty(128, min=128, max=256, errorvalue=128)
    size_text = NumericProperty(10)

    def __init__(self, **kwargs):
        super(Gauge, self).__init__(**kwargs)
            
        self._gauge = Scatter(
            size=(self.size_gauge, self.size_gauge),
            do_rotate=False, 
            do_scale=False,
            do_translation=False
            )

        _img_gauge = Image(source=self.file_gauge, size=(self.size_gauge, 
            self.size_gauge))

        self._needle = Scatter(
            size=(self.size_gauge, self.size_gauge),
            do_rotate=False,
            do_scale=False,
            do_translation=False
            )

        _img_needle = Image(source=self.file_needle, size=(self.size_gauge, 
            self.size_gauge))

        self._glab = Label(font_size=self.size_text, markup=True)
        self._progress = ProgressBar(max=100, height=20, value=self.value)
       
        self._gauge.add_widget(_img_gauge)
        self._needle.add_widget(_img_needle)
        
        self.add_widget(self._gauge)
        self.add_widget(self._needle)
        self.add_widget(self._glab)
        self.add_widget(self._progress)

        self.bind(pos=self._update)
        self.bind(size=self._update)
        self.bind(value=self._turn)
        
    def _update(self, *args):
        '''
        Update gauge and needle positions after sizing or positioning.

        '''
        self._gauge.pos = self.pos
        self._needle.pos = (self.x, self.y)
        self._needle.center = self._gauge.center
        self._glab.center_x = self._gauge.center_x
        self._glab.center_y = self._gauge.center_y + (self.size_gauge/4)
        self._progress.x = self._gauge.x
        self._progress.y = self._gauge.y + (self.size_gauge / 4)
        self._progress.width = self.size_gauge

    def _turn(self, *args):
        '''
        Turn needle, 1 degree = 1 unit, 0 degree point start on 50 value.

        '''
        self._needle.center_x = self._gauge.center_x
        self._needle.center_y = self._gauge.center_y
        self._needle.rotation = (50 * self.unit) - (self.value * self.unit)
        self._glab.text = "[b]{0:.0f}[/b]".format(self.value)
        self._progress.value = self.value


class GaugeApp(App):
        def build(self):
            from kivy.uix.slider import Slider

            def test(*ars):
                gauge.value = s.value
                print(s.value)
            
            box = BoxLayout(orientation='vertical', spacing=10, padding=10)
            gauge = Gauge(value=50, size_gauge=180, size_text=18)
            box.add_widget(gauge)
            
            s = Slider(min=0, max=100, value=50)
            s.bind(value=test)
            box.add_widget(s)
            
            return box
            
if __name__ in ('__main__'):
    GaugeApp().run()