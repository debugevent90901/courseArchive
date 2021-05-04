/* This program finds the roots of the given polynomial in given interval if existed. The parameters includes the five cofficients
of the polynomial and the two bounds of the given interval. The program first finds the numbers of roots in the interval using Budan's 
Theorem and then find the roots using Halley's method. */
/* It accepts a file containing 7 numbers representing a, b, c, d, e (the cofficients of polynomial) and l, r (the left and right bounds
of the interval) from stdin (terminal), and puts a sequence of statements showing the roots with the form of "Root found: root " to stdout
(terminal). If no root exists, the program will print "The polynomial has no roots in the given interval." to stdout (terminal). */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

/* function prototypes */
double abs_double(double y);
double fx_val(double a, double b, double c, double d, double e, double x);
double fx_dval(double a, double b, double c, double d, double e, double x);
double fx_ddval(double a, double b, double c, double d, double e, double x);
double newrfind_halley(double a, double b, double c, double d, double e, double x);
int rootbound(double a, double b, double c, double d, double e, double r, double l);
/* I declare another function calculating the numbers of sign variations to simplify the function rootbound. */
double coffi_val(double a, double b, double c, double d, double e, double x);

/* I declare a global variable root_exist to represent whether the function newrfind_halley has found a root in each call 
in each iteration in main function. If a root is found, the root_exist will be set to 1 and will be restored after output. */
int root_exist = 0; 

int main(int argc, char **argv)
{
    double a, b, c, d, e, l, r;
    FILE *in;

    if (argv[1] == NULL) 
    {
        printf("You need an input file.\n");
        return -1;
    }

    /* this code reads input from a file  -- do not modify it! */
    in = fopen(argv[1], "r");
    if (in == NULL)
        return -1;

    fscanf(in, "%lf", &a);
    fscanf(in, "%lf", &b);
    fscanf(in, "%lf", &c);
    fscanf(in, "%lf", &d);
    fscanf(in, "%lf", &e);
    fscanf(in, "%lf", &l);
    fscanf(in, "%lf", &r);

    fclose(in);
    
    /* The values are read into the variable a, b, c, d, e, l and r.
       You have to find the bound on the number of roots using rootbound function.
       If it is > 0 try to find the roots using newrfind function.
       You may use the fval, fdval and fddval funtions accordingly in implementing the halleys's method.  */

    /* write tour code here */

    int root_num;       /* the upper bound of the numbers of roots in the interval. */

    /* call the function rootbound() to calculate the numbers of roots in the interval. */
    root_num = rootbound(a, b, c, d, e, r, l);                  

    /* if the upper bound is 0, it means the polynomial has no roots in the given interval. */
    if (root_num == 0)
        printf("The polynomial has no roots in the given interval.\n");
    else
    {   
        /* if the upper bound isn't 0, write a loop to iterate the interval with gap=0.5 and call newrfind_halley() to find possible root in each iteration. */
        for (double i = l ; i <= r ; i += 0.5)
        {
            double root;    /* the value of root calculated. */

            /* call newrfind_halley() to find possible root. */
            root = newrfind_halley(a, b, c, d, e, i);

            /* if the global variable is set to 1 in newrfind_halley(), it means a root is found. */ 
            if ((root_exist == 1) && (root <= r) && (root >= l))
            {
                /* output. */
                printf("Root found: %lf\n", root);
                /* restore root_exist to 0 in the end of the iteration. */
                root_exist = 0;
            }
            /* or there's no root with this starting point. */
            else
            {   
                /* output. */
                printf("No roots found.\n");
            }

        }
    }

    return 0;
}

/* implement these functions */

double abs_double(double y)
{
    /* Change this to return the absolute value of y i.e |y| */
    /* this absolute value function use the ternary conditional operator to compare input y with 0. If
    bigger than 0, then output y, else output -y, which is just the absolute value. */
    return (y >= 0) ? y : (-1 * y);
}

double fx_val(double a, double b, double c, double d, double e, double x)
{
    /* Change this to return the value of the polynomial at the value x  */
    /* this function calculate and return the value of the polynomial when the x is input. */
    return (a * pow(x, 4) + b * pow(x, 3) + c * pow(x, 2) + d * x + e);
}

double fx_dval(double a, double b, double c, double d, double e, double x)
{
    /* Change this to return the value of the derivative of the polynomial at the value x */
    /* this function calculate and return the value of the derivative of polynomial when the x is input. */
    return (4 * a * pow(x, 3) + 3 * b * pow(x, 2) + 2 * c * x + d);
}

double fx_ddval(double a, double b, double c, double d, double e, double x)
{
    /* Change this to return the value of the double derivative of the polynomial at the value x */
    /* this function calculate and return the value of the double derivative of polynomial when the x is input. */
    return (12 * a * pow(x, 2) + 6 * b * x + 2 * c);
}

double newrfind_halley(double a, double b, double c, double d, double e, double x)
{
    double appro_cur = x, appro_new = 0.0;  /* approximate root x(n+1) and x(n) used in recursive. */

    /* write a loop to iterate less tham 10000 times. In every iteration use the provided formula to recursive and calculate the next appro_root. */
    for (int i = 1 ; i <= 10000 ; i++)
    {
        /* iterate recursively use the formula provided. */
        appro_new = appro_cur - ((2 * fx_val(a, b, c, d, e, appro_cur) * fx_dval(a, b, c, d, e, appro_cur)) / (2 * pow(fx_dval(a, b, c, d, e, appro_cur), 2) - fx_val(a, b, c, d, e, appro_cur) * fx_ddval(a, b, c, d, e, appro_cur)));
        /* if x(n+1) == x(n) after a certain recursion, it is the root calculated. */ 
        if (abs_double(appro_new - appro_cur) <= 0.000001)
        {
            /* set the global variable root_exist to be 1, meaning one root is calculated. */
            root_exist = 1;
            /* break the loop. */
            break;
        }
        /* assign the x(n+1) to x(n) and prepare for the next recursion. */
        appro_cur = appro_new;
    }
    /* return value is the double type appro_new, the appro_root (if existed), else return -1 (as initialization). */
    /* Change this to return the root found starting from the initial point x using Halley's method */
    return appro_new;
}

int rootbound(double a, double b, double c, double d, double e, double r, double l)
{
    /* this function calculate and return the absolute value of the difference of the sign variations at the 
    bounds of the interval, which calls the function abs_double() and coffi_va;(). */
    /* Change this to return the upper bound on the number of roots of the polynomial in the interval (l, r) */
    return (abs_double(coffi_val(a, b, c, d, e, l) - coffi_val(a, b, c, d, e, r)));
}

/* I define this function to calculate the sign variations, which can be called in other function and thus there's no need to write these 
codes twice when calculating the sign variations of two bounds of the interval. So this mp will be more structured and convenient. */
double coffi_val(double a, double b, double c, double d, double e, double x)
{
    double coffi[5];    /* a double array to store the five cofficients of the polynomial. */
    int sign_vari = 0;  /* the number of the sign variations, initialize to 0. */

    /* assign and store the five cofficients in the array. */
    coffi[0] = a;       
    coffi[1] = 4 * a * x + b;
    coffi[2] = 6 * a * pow(x, 2) + 3 * b * x + c;
    coffi[3] = 4 * a * pow(x, 3) + 3 * b * pow(x, 2) + 2 * c * x + d;
    coffi[4] = a * pow(x, 4) + b * pow(x, 3) + c * pow(x, 2) + d * x + e;

    /* a loop to iterate through the five cofficients to calculate the sign variations. if the continuous two cofficients
    multiplied and is smaller than 0, it will be counted as one sign variation. */
    for (int i = 0 ; i <= 3 ; i++)
        sign_vari = (coffi[i] * coffi[i+1] < 0) ? (sign_vari + 1) : (sign_vari);

    /* return value is the int, the numbers of sign variations. */
    return sign_vari;
}




































