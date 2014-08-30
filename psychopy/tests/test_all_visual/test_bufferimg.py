#!/usr/bin/env python2

# test BufferImageStim quality: a screenshot should not differ from raw stim.draw()
# interpolate makes a big difference for Shapes
# antialias has no effect for Text
# Images seem fine

import pytest
import os
from psychopy.tests import utils
from psychopy import visual, event, core
import numpy as np

imgfile = os.path.join(utils.TESTS_DATA_PATH, 'testimage.jpg')

@pytest.mark.bufferimage
def test_bufferimage_quality():
    scale = {'norm': 1, 'pix': 60, 'cm': 2}
    for units in ['norm', 'pix', 'cm']:
        win = visual.Window(fullscr=False, size=(400, 300), units=units, monitor='testMonitor')
        # nb: virtually no other settings work for rect
        shape = visual.Circle(win, ori=29, radius=.3*scale[units], edges=8, fillColor='blue', interpolate=True, name='shape')
        shape2 = visual.Circle(win, ori=13, radius=.1*scale[units], edges=7, interpolate=False, name='shape2')
        word = visual.TextStim(win, text=u"some text", height=.25*scale[units], antialias=True, name='word')
        word2 = visual.TextStim(win, text=u"(\u03A8 \u040A \u03A3)", height=.15*scale[units], antialias=False, name='word2')
        img = visual.ImageStim(win, size=(scale[units], scale[units]), image=imgfile, name='img', flipVert=True)
        for rect in [(-.6,.6,.6,-.6), (-1,1,1,-1)]:
            for stim in [shape, shape2, word, word2, img]:
                win.clearBuffer()
                stim.draw()
                orig = np.array(win._getRegionOfFrame(buffer='back', mode='RGB'))
                screenshot = visual.BufferImageStim(win, stim=[stim], rect=rect)
                # take a screenshot of a screenshot to exagerate any discrepancies:
                for i in range(20):
                    screenshot = visual.BufferImageStim(win, stim=[screenshot], rect=rect)
                win.clearBuffer()
                screenshot.draw()
                region = np.array(win._getRegionOfFrame(buffer='back', mode='RGB'))
                # display only while create next item
                win.flip()
                err = np.std(region - orig)
                print stim.name, units, rect, '%s, err=%.16f' % (region.shape , err)
                assert err == 0
        win.close()

if __name__ == '__main__':
    test_bufferimage_quality()
