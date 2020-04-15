#!/usr/bin/env python2.7

#######
# Note: This is intended for the Asus Zenbook / Variobook Flip. It was tested on model Zenbook
#       UX463FA, but should work on any tablet with a similar touchscreen (name: 'ELAN9008:00 04F3:29B9'
#       and 'ELAN0732:00 04F3:2493')
#       If it doesn't work, check the output of 'xinput --list', and replace the touchscreen id,
#       trackpad name, and pen (if applicable) at the top of the script with your values.
#       The program was tested under Mint Mate 19.3. For there is a bug in screen presentation
#       after rotation there is a workaround to let caja refresh the screen after rotation
#       forked from: https://github.com/tegan-lamoureux/Rotate-Spectre


from time import sleep
from os import path as op
import sys
from subprocess import check_call, check_output
from glob import glob


# Your device names go here (tested with: xinput --list); use the names,
# the IDs can change depending on conected devices
TOUCHSCREEN = 'pointer:ELAN9008:00 04F3:29B9'
TOUCHPAD    = 'ASUE1407:00 04F3:310D Touchpad'
PEN         = 'ELAN0732:00 04F3:22E1 Pen Pen (0)'
KEYBOARD    = 'AT Translated Set 2 keyboard'

# for Mint Mate we circumvent a bug in Caja which handles presentation of the desktop
MintMateBug = True

def bdopen(fname):
    return open(op.join(basedir, fname))


def read(fname):
    return bdopen(fname).read()


for basedir in glob('/sys/bus/iio/devices/iio:device*'):
    if 'accel' in read('name'):
        break
else:
    sys.stderr.write("Can't find an accellerator device!\n")
    sys.exit(1)


scale = float(read('in_accel_scale'))

g = 7.0  # (m^2 / s) sensibility, gravity trigger

STATES = [
    {'rot': 'normal', 'coord': '1 0 0 0 1 0 0 0 1', 'touchpad': 'enable', 'click': 'double',
     'check': lambda x, y: y <= -g},
    {'rot': 'inverted', 'coord': '-1 0 1 0 -1 1 0 0 1', 'touchpad': 'disable', 'click': 'single',
     'check': lambda x, y: y >= g},
    {'rot': 'left', 'coord': '0 -1 1 1 0 0 0 0 1', 'touchpad': 'disable', 'click': 'single',
     'check': lambda x, y: x >= g},
    {'rot': 'right', 'coord': '0 1 0 -1 0 1 0 0 1', 'touchpad': 'disable', 'click': 'single',
     'check': lambda x, y: x <= -g},
]


def rotate(state):
    s = STATES[state]
    if MintMateBug:
        check_call(['gsettings', 'set', 'org.mate.background', 'show-desktop-icons', 'false'])

    check_call(['xrandr', '-o', s['rot']])
    check_call(['xinput', 'set-prop', TOUCHSCREEN, 'Coordinate Transformation Matrix',] + s['coord'].split())

    if "Pen (0)" in check_output(['xinput', '--list']):
        check_call(['xinput', 'set-prop', PEN, 'Coordinate Transformation Matrix',] + s['coord'].split())

    check_call(['xinput', s['touchpad'], TOUCHPAD])
    check_call(['xinput', s['touchpad'], KEYBOARD])

    if MintMateBug:
        check_call(['gsettings', 'set', 'org.mate.caja.preferences', 'click-policy', s['click']])
        check_call(['gsettings', 'set', 'org.mate.background', 'show-desktop-icons', 'true'])


def read_accel(fp):
    fp.seek(0)
    return float(fp.read()) * scale


if __name__ == '__main__':
    # next if clause adjust the touchpad sensitivity because the values could not been
    # set to prefered values in the GUI, could be deleted if not necessary
    if MintMateBug:
        check_call(['xinput', '--set-prop', TOUCHPAD, '306', '25'])
        check_call(['xinput', '--set-prop', TOUCHPAD, '304', '1.5'])

    accel_x = bdopen('in_accel_x_raw')
    accel_y = bdopen('in_accel_y_raw')

    current_state = 0

    while True:
        x = read_accel(accel_x)
        y = read_accel(accel_y)

        for i in range(4):
            if i == current_state:
                continue
            if STATES[i]['check'](x, y):
                current_state = i
                rotate(i)
                break
        sleep(1)
