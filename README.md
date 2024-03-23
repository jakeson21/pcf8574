```bash
make
sudo i2cdetect -y -a 1 # At 0x20
gpioinfo
sudo dtoverlay pcf8574.dtbo
sudo i2cdetect -y -a 1 # UU at 0x20
gpioinfo # notice gpiochip3 - 8 lines:

sudo dtoverlay -r pcf8574
```

# DTS Reference
https://android.googlesource.com/kernel/msm/+/android-7.1.0_r0.2/Documentation/devicetree/bindings/gpio/gpio-pcf857x.txt
