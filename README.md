# Rotate-ZenbookFlip

This is a small python(2) script for linux that enables auto rotation of the touchscreen (as well as auto-rotation of the touchscreen input mapping) on the latest Asus Zenbook and Variobook Flip models (the newer Kaby Lake model of the HP Spectre x360 should work as well).

It's forked from https://github.com/tegan-lamoureux/Rotate-Spectreand improved to take Asus Zen- and Variobook Flip into account.

For this script to work, you'll have to change device names yourself. The PEN line will only be used if pen support is found, so don't worry about it if yours doesn't have that.

I'm aware that I could have programatically scanned and found the touchscreen name with check_output(), but that was where the first version of this script was failing me, and I don't have access to enough hardware to reliably write that. So manual it is.

Changes in this version:

 - device names adapted
 - keyboard and touchpad are switch off in Tablet and Tent modes
 - circumvents a bug in Mint Mate's Caja that fails in handling the representation of desktop after rotation
 - adjusts acceleration of touchpad at startup (in Mate's GUI tool necessary values not able to adjust)

### Requirements

 - Python 2.7
 - HP Spectre x360, Asus Zenbook Flip UX463FA (But honestly, it might work with others if the correct devices are passed. Give it a shot.)

### Usage

Find the names of your devices with `xinput --list`, and compare the names for your touchscreen, trackpad, keyboard and / or pen with the variables `TOUCHSCREEN`, `TOUCHPAD`, `KEYBOARD` and / or `PEN` (if applicable) at the top of the script. Replace if necessary. Set MintMateBug to False if different DE is used.

Run as a script (after making executable) with `./rotate.py &`, or by using python directly with `python2.7 rotate.py &`. For persistence after reboot, ensure it runs after starting the Desktop Environment, however that's done with your distribution. For Mint Mate (and others Gnome based DEs) that's usually done by placing a .desktop file in folder $HOME/.config/autostart, for Arch that's in `~/.xinit` before you exec your xorg/wm/dm.

### Troubleshooting

Double check your names, make sure you're updated to the latest version of whatever kernel your distro runs, and make sure you're using Python 2. If it's still giving you an error, feel free to email or open an issue!
