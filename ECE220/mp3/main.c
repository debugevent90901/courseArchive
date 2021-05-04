/* This program calculate the values of a signal after low-pass filter with the given parameters omega1, omega2, omegac and 
method using finite difference method(if method = 1) or Runge-Kutta method(if method = 2). */
/* It accepts a file containing 4 numbers representing omega1, omega2, omegac and method from stdin (terminal), and puts a 
sequence of float numbers to stdout (terminal). */ 

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

/* Write your code under the two if statements indicated below. */
int main(int argc, char **argv)
{
    double omega1, omega2, omegac, T, dt;
    int N, method;
    FILE *in;

    int i;
    double Voutnew = 0.0, Voutcur = 0.0, Voutprev = 0.0;

    /* If implementing method 2 for challenge, declare additional variables here */

    double m1, m2, m3, m4;                      /* cofficients m1, m2, m3, m4 in provided formulas */
    double k1, k2, k3, k4;                      /* cofficients k1, k2, k3, k4 in provided formulas */
    double Vout1new = 0.0, Vout1cur = 0.0;      /* V_out1 in the provided formulas and initialize to 0, -new and -cur are used to recursive */
    double Vout2new = 0.0, Vout2cur = 0.0;      /* V_out2 in the provided formulas and initialize to 0, -new and -cur are used to recursive */

        
    /* Open the file and scan the input variables. */
    if (argv[1] == NULL) 
    {
        printf("You need an input file.\n");
        return -1;
    }

    if ((in = fopen(argv[1], "r")) == NULL)
    {
        printf("Unable to open specified file %s\n", argv[1]);
        return -1;
    }

    fscanf(in, "%lf", &omega1);
    fscanf(in, "%lf", &omega2);
    fscanf(in, "%lf", &omegac);
    fscanf(in, "%d", &method);

    fclose(in);

    T = 3 * 2 * M_PI / omega1; 	        /* Total time */
    N = 20 * T / (2 * M_PI / omega2);   /* Total number of time steps */
    dt = T / N;                         /* Time step ("delta t") */

    /* Method number 1 corresponds to the finite difference method. */
    if (method == 1) 
    {
        /* Write your code here! */
        /* define three variables to express the cofficients in the formula so the expression in single line won't be too long */
        double coe1, coe2, coe3;
        /* a main loop to iterate n(i in the expression) and respectively calaulate and output the Vout in every iteration */
        for (i = 0 ; i < N ; i++)
        {
            /* assign values to declared cofficients in the provided formula */
            coe1 = 1 / (1 / dt / omegac / sqrt(2) + 1 / dt / dt / omegac / omegac);
            coe2 = 2 / dt / dt / omegac / omegac - 1;
            coe3 = 1 / dt / omegac / sqrt(2) - 1 / dt / dt / omegac / omegac;

            /* calculate the Vout(n+1) using the current state and previous state Vout(n) and Vout(n-1) */
            Voutnew = coe1 * (coe2 * Voutcur + coe3 * Voutprev + sin(omega1 * i * dt) + 0.5 * sin(omega2 * i * dt));

            /* Output Vout */
            printf("%lf\n", Voutcur);

            /* assign the n(current) state to n-1(previous) state, the n+1(new) state to n(current) state for next iteration */ 
            Voutprev = Voutcur;
            Voutcur = Voutnew;
        }

    }

    /* Method number 2 corresponds to the Runge-Kutta method (only for challenge). */
    else if (method == 2) 
    {
        /* Write your code here for the challenge problem. */
        /* a main loop to iterate n(i in the expression) and respectively calaulate the Vout1, Vout2 and output Vout1 in every iteration */
        for (i = 0 ; i < N ; i++)
        {

            /* assign values to declared cofficients in the first provided formula */
            k1 = Vout2cur;
            k2 = Vout2cur + 0.5 * k1 * dt;
            k3 = Vout2cur + 0.5 * k2 * dt;
            k4 = Vout2cur + k3 * dt;

            /* assign values to declared cofficients in the second provided formula */
            m1 = omegac * omegac * (sin(omega1 * i * dt) + 0.5 * sin(omega2 * i * dt)) - omegac * omegac * Vout1cur - omegac * sqrt(2) * Vout2cur;
            m2 = m1 * (1 + 0.5 * dt);
            m3 = m1 + 0.5 * m2 * dt;
            m4 = m1 + m3 * dt;

            /* calculate the Vout1(n+1) and Vout2(n+1) using the current state Vout1(n) */
            Vout1new = Vout1cur + (k1 + 2 * k2 + 2 * k3 + k4) * dt / 6;
            Vout2new = Vout2cur + (m1 + 2 * m2 + 2 * m3 + m4) * dt / 6;

            /* Output Vout1 */
            printf("%lf\n", Vout1cur);

            /* assign the n+1(new) state to n(current) state of Vout1 and Vout2 for next iteration */ 
            Vout1cur = Vout1new;
            Vout2cur = Vout2new;
        }

    }

    else 
    {
        printf("Incorrect method number.\n");
        return -1;
    }

    return 0;
}
