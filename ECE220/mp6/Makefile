all:
	gcc -Wall -g  main.c updateBoard.c -o gameoflife -lncurses
	gcc -Wall -g test.c updateBoard.c updateBoardGold.o -o test
clean:
	rm gameoflife
	rm test
