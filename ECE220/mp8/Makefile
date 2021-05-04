
mp8: main.c sudoku.c
	gcc -g -c sudoku.c -o sudoku.o
	gcc -g -c main.c -o main.o
	gcc -g main.o sudoku.o sudoku_golden.a -o mp8

clean:
	rm -f *.o mp8

sudoku1: mp8
	./mp8 sudoku1.txt

sudoku2: mp8
	./mp8 sudoku2.txt

sudoku3: mp8
	./mp8 sudoku3.txt
