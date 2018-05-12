'''
AC v1.14.3 x64

Use:
- ac.freeCameraRotateHeading(angle)
- ac.freeCameraRotateRoll(angle)
- ac.freeCameraRotatePitch(angle)
to control camera rotation

WBR, kasperski95
'''

import ac
import os
import math
import ctypes
import sys
import linecache
from ctypes import*

class CamToolTool(object):
    def __init__(self):
        self.__path = WinDLL( (os.path.abspath(__file__)+'CamTool_1-16.dll').replace("\\",'/').replace( os.path.basename(__file__),'') )

    def is_lmb_pressed(self):
        self.__path.IsLeftMouseButtonPressed.restype = ctypes.c_bool
        return self.__path.IsLeftMouseButtonPressed()

    def is_async_key_pressed(self, value):
        self.__path.IsAsyncKeyPressed.argtypes = [ctypes.c_wchar]
        self.__path.IsAsyncKeyPressed.restype = ctypes.c_bool
        return self.__path.IsAsyncKeyPressed(value)

    def get_position(self, axis):
        self.__path.GetPosition.restype = ctypes.c_float
        return self.__path.GetPosition(axis)

    def set_position(self, axis, value):
        self.__path.SetPosition.argtypes = [ctypes.c_int, ctypes.c_float]
        self.__path.SetPosition.restype = ctypes.c_bool
        return self.__path.SetPosition(axis, value)

    def get_heading(self):
        self.__path.GetHeading.restype = ctypes.c_float
        return (-1) * self.__path.GetHeading()

    def set_heading(self, angle, absolute=True):
        try:
            self.prev_pitch = self.get_pitch()
            self.prev_roll = self.get_roll()
            ac.freeCameraRotateRoll(0 - self.prev_roll)
            ac.freeCameraRotatePitch(0 - self.prev_pitch)

            if absolute:
                ac.freeCameraRotateHeading( angle - self.get_heading() )
            else:
                ac.freeCameraRotateHeading(angle)

            ac.freeCameraRotatePitch(self.prev_pitch)
            ac.freeCameraRotateRoll(self.prev_roll)

            return 1

        except Exception as e:
            debug(e)

    def get_pitch(self):
        self.__path.GetPitch.restype = ctypes.c_float
        return self.__path.GetPitch()

    def set_pitch(self, angle, absolute=True):
        self.prev_roll = self.get_roll()
        self.set_roll( 0 )
        if absolute:
            ac.freeCameraRotatePitch( angle - self.get_pitch() )
        else:
            ac.freeCameraRotatePitch( angle )
        self.set_roll( self.prev_roll )
        return 1

    def set_heading_and_pitch(self, heading, pitch): #optimization
        self.prev_roll = self.get_roll()
        self.set_roll(0)
        ac.freeCameraRotatePitch(0 - self.get_pitch())
        ac.freeCameraRotateHeading(heading - self.get_heading())
        ac.freeCameraRotatePitch(pitch)
        self.set_roll(self.prev_roll)

    def set_rotation(self, pitch, roll, heading):
        ac.freeCameraRotateRoll(0 - self.get_roll())
        ac.freeCameraRotatePitch(0 - self.get_pitch())
        ac.freeCameraRotateHeading(heading - self.get_heading())
        ac.freeCameraRotatePitch(pitch)
        ac.freeCameraRotateRoll(roll)

    def get_roll(self):
        self.__path.GetRoll.restype = ctypes.c_float
        return math.asin( max(-1, min(1, self.__path.GetRoll() )) )

    def set_roll(self, angle, absolute=True):
        if absolute:
            ac.freeCameraRotateRoll( angle - self.get_roll())
        else:
            ac.freeCameraRotateRoll( angle )
        return 1


    def get_fov(self):
        self.__path.GetFOV.restype = ctypes.c_float
        return self.__path.GetFOV()

    def convert_fov_2_focal_length(self, val, reverse=False):
        #convert to interpolation freindly format

        if val != 0:
            self.x = 15
            if not reverse:
                return 1 / (val + self.x)
            else:
                return (1 - self.x * val) / val

        return 0.00001

        # if reverse:
        #     return 2203 / (2 * math.tan(math.pi * val / 360))
        # else:
        #     return 2 * math.atan(2203 / (2 * val)) * 180 / math.pi

    def set_fov(self, fov):
        self.__path.SetFOV.argtypes = [ctypes.c_float]
        self.__path.SetFOV.restype = ctypes.c_bool

        self.near_clipping = min(2, max(0.1, (2 - (fov/50))))

        self.set_clipping_near(self.near_clipping)

        return self.__path.SetFOV(fov)

    def get_dof_factor(self):
        self.__path.GetDOFfactor.restype = ctypes.c_int
        return self.__path.GetDOFfactor()

    def set_dof_factor(self, strength):
        self.__path.SetDOFfactor.argtypes = [ctypes.c_int]
        self.__path.SetDOFfactor.restype = ctypes.c_bool
        return self.__path.SetDOFfactor(strength)

    def get_focus_point(self):
        self.__path.GetFocusPoint.restype = ctypes.c_float
        return self.__path.GetFocusPoint()

    def set_focus_point(self, value):
        self.__path.SetFocusPoint.argtypes = [ctypes.c_float]
        self.__path.SetFocusPoint.restype = ctypes.c_bool
        if value < 0.1:
            self.set_dof_factor( 0 )
        else:
            self.set_dof_factor( 1 )
        return self.__path.SetFocusPoint(value)

    def set_clipping_near(self, clipping):
        self.__path.SetClippingNear.argtypes = [ctypes.c_float]
        self.__path.SetClippingNear.restype = ctypes.c_bool
        return self.__path.SetClippingNear(clipping)

    def set_clipping_far(self, clipping):
        self.__path.SetClippingFar.argtypes = [ctypes.c_float]
        self.__path.SetClippingFar.restype = ctypes.c_bool
        return self.__path.SetClippingFar(clipping)

    def get_replay_position(self):
        self.__path.GetReplayPosition.restype = ctypes.c_int
        return self.__path.GetReplayPosition()

    def set_replay_position(self, keyframe):
        self.__path.SetReplayPosition.argtypes = [ctypes.c_int]
        self.__path.SetReplayPosition.restype = ctypes.c_bool
        return self.__path.SetReplayPosition(keyframe)

    def set_replay_speed(self, value):
        self.__path.SetReplaySpeed.argtypes = [ctypes.c_float]
        self.__path.SetReplaySpeed.restype = ctypes.c_bool
        return self.__path.SetReplaySpeed(value)

    def get_volume(self):
        self.__path.GetVolume.restype = ctypes.c_float
        return self.__path.GetVolume()




    def set_volume(self, value):
        self.__path.SetVolume.argtypes = [ctypes.c_float]
        self.__path.SetVolume.restype = ctypes.c_bool
        return self.__path.SetVolume(value)

ctt = CamToolTool()

def debug(e):
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    #ac.console( 'CamTool 2: EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj) )
    ac.console( 'CamTool 2: EXCEPTION IN (LINE {}): {}'.format(lineno, exc_obj) )
    ac.log( 'CamTool 2: EXCEPTION IN ({} LINE {}): {}'.format(filename, lineno, exc_obj) )
