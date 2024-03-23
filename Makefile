obj-m += pcf8574.o

all: dt main
	echo Built Device Tree Overlay

dt: pcf8574.dts
	dtc -@ -I dts -O dtb -o pcf8574.dtbo pcf8574.dts

main: main.c
	gcc main.c -g -O0 -lgpiod -o main

clean:
	rm -rf pcf8574.dtbo main
	
