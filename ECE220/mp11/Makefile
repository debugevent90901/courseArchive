CC := gcc
CFLAGS :=-Wall -g
LDFLAGS := -g -lm
HEADERS := visualize.h mp11.h Makefile
EXE := mp11
SOURCES := mp11.o mp11match.o mp11main.o

.ALL: ${EXE}

%.o: %.c ${HEADERS} Makefile
	${CC} -c ${CFLAGS} -o $@ $<

${EXE}: ${SOURCES}
	$(CC) ${SOURCES} -o ${EXE} ${LDFLAGS}

result.c: mp11 Makefile graph requests
	./mp11 graph requests

view_result: mp11 visualize.o visualize-main.o result.o ${HEADERS}
	${CC} ${CFLAGS} -o $@ visualize.o visualize-main.o result.o -lpng

image.png: view_result
	./view_result

image: image.png

clean::
	rm -f ${SOURCES} visualize.o visualize-main.o result.o result.c

clear: clean
	rm -f ${EXE} image.png view_result
