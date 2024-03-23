#include <gpiod.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <signal.h>
#include <time.h>


static volatile int run = 1;

void intHandler(int dummy) {
    run = 0;
}

int open_gpio(char *chipname, struct gpiod_chip **chip, struct gpiod_line **line, unsigned int line_num, char *line_name)
{
    *chip = gpiod_chip_open_by_name(chipname);
    if (!*chip) {
        perror("Open chip failed\n");
        return -1;
    }

    *line = gpiod_chip_get_line(*chip, line_num);
    if (!*line) {
        perror("Get line failed\n");
        return -1;
    }

    int ret = gpiod_line_request_output(*line, line_name, 0);
	if (ret < 0) {
		perror("Request line as output failed\n");
		return -1;
	}

    return ret;
}

int main(int argc, char **argv)
{
	char chipname[] = "gpiochip3";
	unsigned int line_num = 0;	// GPIO Pin #0
	unsigned int val;
	struct gpiod_chip *chip;
	struct gpiod_line *line;
	int i, ret;

    signal(SIGINT, intHandler);

    if (open_gpio(chipname, &chip, &line, line_num, "MyLine123456789012345678901234567890") != 0)
    {
        goto release_line;
    }

    // chip = gpiod_chip_open_by_name(chipname);
    // if (!chip) {
    // 	perror("Open chip failed\n");
    // 	goto end;
    // }

    // line = gpiod_chip_get_line(chip, line_num);
    // if (!line) {
    // 	perror("Get line failed\n");
    // 	goto close_chip;
    // }

    // ret = gpiod_line_request_output(line, "Test", 0);
    // if (ret < 0) {
    // 	perror("Request line as output failed\n");
    // 	goto release_line;
    // }

	/* Blink */
	val = 0;
	while (run) {
		ret = gpiod_line_set_value(line, val);
		if (ret < 0) {
			perror("Set line output failed\n");
			goto release_line;
		}
		// printf("Output %u on line #%u\n", val, line_num);
		// nanosleep(00);
		val = !val;
	}

release_line:
    if (line) gpiod_line_release(line);
close_chip:
    if (chip) gpiod_chip_close(chip);
end:
	return 0;
}