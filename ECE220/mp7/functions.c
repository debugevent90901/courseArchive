/* 
 * This .c file contains 10 functions essential to edit an image.
 *  
 * The getRadius function calculates and returns the radius value in int, which accepts one parameter sigma typed in double.
 * 
 * The calculateGausFilter function is aimed to create the Gaussian fliter. It accepts sigma as parameter, and stores the fliter in another 
 * parameter *gausFliter, which is an array already set its memory location.
 * 
 * The convolveImage function is aimed to apply Gaussian fliter to the input image. It accepts *inRed, *inGreen, *inBlue, *inAlpha, *outRed
 * , *outGreen, *outBlue, *outAlpha, *filter, radius, width, height as parameters and the output data will be stored in four *out arrays.
 *
 * The convertToGray function is aimed to Converts the image to gray scale. Each pixel will be set to the weighted average according to the 
 * formula 0.299R + 0.587G + 0.114B. Alpha channel will be retained from the input image. The output will be stored in four *out arrays.
 *
 * The invertImage function is aimed to Inverts the value of the pixel p, in each channel to 255 - p. Alpha channel is not inverted but just 
 * copied from the input channel. The output will be stored in four *out arrays.
 * 
 * The pixelate function is aimed to create a pixelated image using the pixelX/Y parameters to create a block of pixelX*pixelY dimensions,
 * overlaid repeatedly from the upper left corner of the image. Set the color of each block to the average color of all pixels in the block 
 * including the alpha channel. At the boundaries, use only the available pixels. The output will be stored in four *out arrays.
 *
 * The colorDodge function is aimed to blends two images together. Formula ((top == 255) ? top : min(((bottom << 8) / (255 - top)), 255)) is provided.
 * And the Alpha channel will be set to to that of the bottom channel. The output will be stored in four *out arrays.
 *
 * The pencilSketch function is a simple function that calls on other helper function.The function convert the input image to grayscale and invert it,
 * apply a Gaussian blur to the input image, and then use the colorDodge function to combine these two images together. The bulurred image should be the 
 * bottom layer while the inverted grayscale should be the top. The output will be stored in four *out arrays.
 *
 * The transformImage function is aimed to apply a linear transformation to the image by changing the locations of the pixels. e.g. scale, rotate, skew,
 * and shift the image in two-dimensional space. The output will be stored in four *out arrays.
 *
 * The nearestPixel function is aimed to compute the nearest pixel in the original image for each pixel of the output image using linear transformation. 
 * The output pixel is stored in two pointers.
 */ 

#include "functions.h"

/*
 * getRadius - returns the radius based on the sigma value
 * INPUTS: sigma - sigma in the Guassian distribution
 * OUTPUTS: none
 * RETURN VALUE: radius - radius of the filter
 */
int getRadius(double sigma)
{
  /* Write your function here. */
  /* a simple function that returns 3 * sigma. */
  /* Since sigma is typed in double, there should be an int() to transform the data type. */
  return int(ceil(3 * sigma));
}

/*
 * calculateGausFilter - calculates the Gaussian filter
 * INTPUTS: gausFitler - pointer to the array for the gaussian filter
 *          sigma - the sigma in the Gaussian distribution
 * OUTPUTS: none
 * RETURN VALUE: none
 */
void calculateGausFilter(double *gausFilter,double sigma)
{
  /* Write your function here. */
  double weight = 0;                                    /* the value of each element, aka "weight". */ 
  int r = getRadius(sigma);                             /* the radius of the Gaussian fliter. */

  /* a traversal through the entire fliter using two loop, one in width, the other in height. */
  for (int m = 0 ; m <= 2 * r ; m++)
  {
    for (int n = 0 ; n <= 2 * r ; n++)
    {
      double dist = pow((r - m), 2) + pow((r - n), 2);  /* (x^2 + y^2), the square of the distance between the center and the current point. */
      /* assign the value of Gaussian function to the current address in fliter. */
      gausFilter[n * (2 * r + 1) + m] = 1 / sqrt(2 * M_PI * pow(sigma, 2)) * exp(-1 / (2 * pow(sigma, 2)) * dist);
      /* increment the weight. */
      weight += gausFilter[n * (2 * r + 1) + m];
    }
  }

  /* another traversal through the entire fliter. */
  for (int i = 0 ; i <= (2 * r + 1) * (2 * r + 1) - 1 ; i++)
    /* normalize the Gaussian filter. */
    gausFilter[i] /= weight; 
  /* the function has no return value. */
  return;
}

/* convolveImage - performs a convolution between a filter and image
 * INPUTS: inRed - pointer to the input red channel
 *         inGreen - pointer to the input green channel
 *         inBlue - pointer to the input blue channel
 *         inAlpha - pointer to the input alpha channel
 *         filter - pointer to the convolution filter
 *         radius - radius of the convolution filter
 *         width - width of the input image
 *         height - height of the input image
 * OUTPUTS: outRed - pointer to the output red channel
 *          outGreen - pointer to the output green channel
 *          outBlue - pointer to the output blue channel
 *          outAlpha - pointer to the output alpha channel
 * RETURN VALUES: none
 */
void convolveImage(uint8_t *inRed,uint8_t *inGreen,uint8_t *inBlue,
                   uint8_t *inAlpha, uint8_t *outRed,uint8_t *outGreen,
                   uint8_t *outBlue,uint8_t *outAlpha,const double *filter,
                   int radius,int width,int height)
{
  /* Write your function here. */
  /* Alpha channel is unchanged anyway, so copy it to output channel at first use a loop. */
  for (int i = 0 ; i <= width * height -1 ; i++)
      outAlpha[i] = inAlpha[i];

  /* if the raduis is less thsan 1, all other channels are unchanged. */
  if (radius < 1)
  {
    /* a traversal through the other channels use a loop. */
    for (int j = 0 ; j <= width * height -1 ; j++)
    {
      /* copy the values in each pixel to output channels. */
      outRed[j] = inRed[j];
      outGreen[j] = inGreen[j];
      outBlue[j] = inBlue[j];
    }
  }

  /* else apply the Guassian fliter. */
  else
  {
    /* a traversal through the input RGB channels using two loop, one in width, the other in height. */
    for (int m = 0 ; m <= width - 1 ; m++)
    {
      for (int n = 0 ; n <= height - 1 ; n++)
      {
        double valR = 0, valG = 0, valB = 0;  /* the value of convolution typed in double, initialize to 0. */

        /* another traversal through the fliter using two loops in width and height, matching with channels to process convolution. */
        for (int p = 0 ; p <= 2 * radius ; p++)
        {
          for (int q = 0 ; q <= 2 * radius ; q++)
          {
            /* the index mapping to the channels should not out of bound. */
            if (((n - radius + q) >= 0) && ((n - radius + q) <= (height -1)) && ((m - radius + p) >= 0) && ((m - radius + p) <= (width - 1)))
            {
              /* calculate and increase the convolution value typed in double stored in each pixel. */
              valR += inRed[(n - radius + q) * width + (m - radius + p)] *  filter[q * (2 * radius + 1) + p];
              valG += inGreen[(n - radius + q) * width + (m - radius + p)] * filter[q * (2 * radius + 1) + p];
              valB += inBlue[(n - radius + q) * width + (m - radius + p)] * filter[q * (2 * radius + 1) + p];
            }
          }  
        }

        /* assign the calculated value of each pixel to output channels, should be bigger than 0, smaller than 255. */
        outRed[n * width + m] = uint8_t(min(max(valR, 0), 225));
        outGreen[n * width + m] = uint8_t(min(max(valG, 0), 225));
        outBlue[n * width + m] = uint8_t(min(max(valB, 0), 225));
        }
    }
  }
/* the function has no return value. */
  return;
}

/* convertToGray - convert the input image to grayscale
 * INPUTS: inRed - pointer to the input red channel
 *         inGreen - pointer to the input green channel
 *         inBlue - pointer to the input blue channel
 *         inAlpha - pointer to the input alpha channel
 *         gMonoMult - pointer to array with constants to be multipiled with 
 *                     RBG channels to convert image to grayscale
 *         width - width of the input image
 *         height - height of the input image
 * OUTPUTS: outRed - pointer to the output red channel
 *          outGreen - pointer to the output green channel
 *          outBlue - pointer to the output blue channel
 *          outAlpha - pointer to the output alpha channel
 * RETURN VALUES: none
 */
void convertToGray(uint8_t *inRed,uint8_t *inGreen,uint8_t *inBlue,
                   uint8_t *inAlpha,uint8_t *outRed,uint8_t *outGreen,
                   uint8_t *outBlue,uint8_t *outAlpha,
                   const double *gMonoMult,int width,int height)
{
  /* Challenge- Write your function here. */
  /* a traversal through the input channels using a loop. */
  for (int i = 0 ; i <= width * height -1 ; i++)
  {
    double gray; /* the value of current pixel in gray scale. */
    /* calculate the gray scale with provided formula in each pixel. */
    gray = inRed[i] * gMonoMult[0] + inGreen[i] * gMonoMult[1] + inBlue[i] * gMonoMult[2];

    /* assign the calculated gray scale of each pixel to RGB output channels. */
    /* since gray is typed in double, convert it to uint8_t. */
    outRed[i] = uint8_t(gray);
    outGreen[i] = uint8_t(gray);
    outBlue[i] = uint8_t(gray);
    /* the Alpha channel remains unchanged as description. */
    outAlpha[i] = inAlpha[i];
  }
  /* the function has no return value. */
  return;
}

/* invertImage - inverts the colors of the image
 * INPUTS: inRed - pointer to the input red channel
 *         inGreen - pointer to the input green channel
 *         inBlue - pointer to the input blue channel
 *         inAlpha - pointer to the input alpha channel
 *         width - width of the input image
 *         height - height of the input image
 * OUTPUTS: outRed - pointer to the output red channel
 *          outGreen - pointer to the output green channel
 *          outBlue - pointer to the output blue channel
 *          outAlpha - pointer to the output alpha channel
 * RETURN VALUES: none
 */
void invertImage(uint8_t *inRed,uint8_t *inGreen,uint8_t *inBlue,
                 uint8_t *inAlpha,uint8_t *outRed,uint8_t *outGreen,
                 uint8_t *outBlue,uint8_t *outAlpha,int width,int height)
{
  /* Challenge- Write your function here. */
  /* a traversal through the input channels using a loop. */
  for (int i = 0 ; i <= width * height -1 ; i++)
  {
    /* calculate and assign the invert value of RGB channels in each pixel, which is the original value substracted by 255. */
    outRed[i] = 255 - inRed[i];
    outGreen[i] = 255 - inGreen[i];
    outBlue[i] = 255 - inBlue[i];
    /* the Alpha channel remains unchanged as description. */
    outAlpha[i] = inAlpha[i];
  }
  /* the function has no return value. */
  return;
}

/* pixelate - pixelates the image
 * INPUTS: inRed - pointer to the input red channel
 *         inGreen - pointer to the input green channel
 *         inBlue - pointer to the input blue channel
 *         inAlpha - pointer to the input alpha channel
 *         pixelateY - height of the block
 *         pixelateX - width of the block
 *         width - width of the input image
 *         height - height of the input image
 * OUTPUTS: outRed - pointer to the output red channel
 *          outGreen - pointer to the output green channel
 *          outBlue - pointer to the output blue channel
 *          outAlpha - pointer to the output alpha channel
 * RETURN VALUES: none
 */
void pixelate(uint8_t *inRed,uint8_t *inGreen,uint8_t *inBlue,uint8_t *inAlpha,
              uint8_t *outRed,uint8_t *outGreen,uint8_t *outBlue,
              uint8_t *outAlpha,int pixelY,int pixelX,int width,int height)
{
  /* Challenge- Write your function here. */
  /* a traversal through the input channels using two loop, one in width, the other in height. */
  /* every time the pixelX and pixelY are the increment. */
  for (int m = 0 ; m <= width - 1 ; m += pixelX)
  {
    for (int n = 0 ; n <= height - 1 ; n += pixelY)
    {
      int sumR = 0, sumG = 0, sumB = 0, sumA = 0; /* the sum of color in the given block of pixels. */

      /* a traversal through the current block using two loops in width and height. */
      for (int p = m ; p <= m + pixelX - 1; p++)
      {
        for (int q = n; q <= n + pixelY - 1 ; q++)
        {
          /* the current index of the pixel inside the block should not out of the bound. */
          if (p >= 0 && q >= 0 && p <= width - 1 && q <= height - 1)
          {
            /* increase the sum of each RGB channel. */
            sumR += inRed[q * width + p];
            sumG += inGreen[q * width + p];
            sumB += inBlue[q * width + p];
            sumA += inAlpha[q * width + p];
          }
        }
      }

      /* another traversal through the current block using two loop in width and height. */ 
      for (int i = m ; i <= m + pixelX - 1; i++)
      {
        for (int j = n; j <= n + pixelY - 1 ; j++)
        {
          /* the current index of the pixel inside the block should still not out of the bound. */
          if (i >= 0 && j >= 0 && i <= width - 1 && j <= height - 1)
          {
            /* assign the average of the sum of each channel to the corresponding pixels in output channels. */
            outRed[j * width + i] = sumR / (pixelX * pixelY);
            outGreen[j * width + i] = sumG / (pixelX * pixelY);
            outBlue[j * width + i] = sumB / (pixelX * pixelY);
            outAlpha[j * width + i] = sumA / (pixelX * pixelY);
          }
        }
      }
    }
  }
  /* the function has no return value. */
  return;
}

/* colorDodge - blends the bottom layer with the top layer
 * INPUTS: aRed - pointer to the bottom red channel
 *         aGreen - pointer to the bottom green channel
 *         aBlue - pointer to the bottom blue channel
 *         aAlpha - pointer to the bottom alpha channel
 *         bRed - pointer to the top red channel
 *         bGreen - pointer to the top green channel
 *         bBlue - pointer to the top blue channel
 *         bAlpha - pointer to the top alpha channel
 *         width - width of the input image
 *         height - height of the input image
 * OUTPUTS: outRed - pointer to the output red channel
 *          outGreen - pointer to the output green channel
 *          outBlue - pointer to the output blue channel
 *          outAlpha - pointer to the output alpha channel
 * RETURN VALUES: none
 */
void colorDodge(uint8_t *aRed,uint8_t *aGreen,uint8_t *aBlue,
                uint8_t *aAlpha,uint8_t *bRed,uint8_t *bGreen,
                uint8_t *bBlue,uint8_t *bAlpha,uint8_t *outRed,
                uint8_t *outGreen,uint8_t *outBlue,uint8_t *outAlpha,
                int width,int height)
{
  /* Challenge- Write your function here. */
  /* a traversal through the input channels using a loop. */
  for (int i = 0 ; i <= width * height -1 ; i++)
  {
    /* assign the output values to each pixel in the output RGB channels use the provided formula. */
    outRed[i] = ((bRed[i] == 255) ? bRed[i] : min(((aRed[i] << 8) / (255 - bRed[i])), 255));
    outGreen[i] = ((bGreen[i] == 255) ? bGreen[i] : min(((aGreen[i] << 8) / (255 - bGreen[i])), 255));
    outBlue[i] = ((bBlue[i] == 255) ? bBlue[i] : min(((aBlue[i] << 8) / (255 - bBlue[i])), 255));
    /* set the alpha channel to the bottom channel. */
    outAlpha[i] = aAlpha[i];
  }
  /* the function has no return value. */
  return;
}

/* pencilSketch - creates a pencil sketch of the input image
 * INPUTS: inRed - pointer to the input red channel
 *         inGreen - pointer to the input green channel
 *         inBlue - pointer to the input blue channel
 *         inAlpha - pointer to the input alpha channel
 *         invRed - pointer to temporary red channel for inversion
 *         invGreen - pointer to temporary green channel for inversion
 *         invBlue - pointer to temporary blue channel for inversion
 *         invAlpha - pointer to temporary alpha channel for inversion
 *         blurRed - pointer to temporary red channel for blurring
 *         blurGreen - pointer to temporary green channel for blurring
 *         blurBlue - pointer to temporary blue channel for blurring
 *         blurAlpha - pointer to temporary alpha channel for blurring
 *         filter - pointer to the gaussian filter to blur the image
 *         radius - radius of the gaussian filter
 *         width - width of the input image
 *         height - height of the input image
 *         gMonoMult - pointer to array with constants to be multipiled with 
 *                     RBG channels to convert image to grayscale
 * OUTPUTS: outRed - pointer to the output red channel
 *          outGreen - pointer to the output green channel
 *          outBlue - pointer to the output blue channel
 *          outAlpha - pointer to the output alpha channel
 * RETURN VALUES: none
 */
void pencilSketch(uint8_t *inRed,uint8_t *inGreen,uint8_t *inBlue,
                  uint8_t *inAlpha,uint8_t *invRed,uint8_t *invGreen,
                  uint8_t *invBlue,uint8_t *invAlpha,uint8_t *blurRed,
                  uint8_t *blurGreen,uint8_t *blurBlue,uint8_t *blurAlpha,
                  uint8_t *outRed,uint8_t *outGreen,uint8_t *outBlue,
                  uint8_t *outAlpha,const double *filter,int radius,int width,
                  int height,const double *gMonoMult)
{
  /* Challenge- Write your function here. */
  /* call the function convertToGray to convert the input image to gray scale and output to *inv. */
  convertToGray(inRed, inGreen, inBlue, inAlpha, invRed, invGreen, invBlue, invAlpha,
                gMonoMult, width, height);
  /* call the function invertImage to perform invert in *inv. */
  invertImage(invRed, invGreen, invBlue, invAlpha, invRed, invGreen, invBlue, invAlpha,
              width, height);
  /* call the function convolveImage to apply a Gaussian fliter to input image and output to *blur. */
  convolveImage(inRed, inGreen, inBlue, inAlpha, blurRed, blurGreen, blurBlue, blurAlpha,
                filter, radius, width, height);
  /* call the function colorDodge to combine two images together with *blur in bottom and *inv in top. */
  colorDodge(blurRed, blurGreen, blurBlue, blurAlpha, invRed, invGreen, invBlue, invAlpha,
             outRed, outGreen, outBlue, outAlpha, width, height);
  /* the function has no return value. */
  return;
}

/* transformImage - Computes an linear transformation of the input image
 * INPUTS: inRed - pointer to the input red channel
 *         inGreen - pointer to the input green channel
 *         inBlue - pointer to the input blue channel
 *         inAlpha - pointer to the input alpha channel
 *	       transform - two dimensional array containing transform coefficients of matrix T and vector S
 *         width - width of the input and output image
 *         height - height of the input and output image
 * OUTPUTS: outRed - pointer to the output red channel
 *          outGreen - pointer to the output green channel
 *          outBlue - pointer to the output blue channel
 *          outAlpha - pointer to the output alpha channel
 * RETURN VALUES: none
 */
void transformImage(uint8_t *inRed,uint8_t *inGreen,uint8_t *inBlue,uint8_t *inAlpha,
              uint8_t *outRed,uint8_t *outGreen,uint8_t *outBlue,
              uint8_t *outAlpha,double transform[2][3],int width,int height)
{
  /* Write your function here. */ 
  int x, y;                         /* the coodinate of x and y in input image. */
  int *pixelX = &x, *pixelY = &y;   /* the pointer to x,y. */

  /* a traversal through the output image using two loop, one in width, the other in height. */
  for (int m = 0 ; m <= width - 1 ; m++)
  {
    for (int n = 0 ; n <= height - 1 ; n++)
    {
      /* call the function nearestPixel to calculte the corresponding coodinate of each pixel in input image. */
      nearestPixel(n, m, transform, pixelY, pixelX, width, height);

      /* if out of bound, set output image's RGB channels to be 0 and Alpha channel to be 255. */
      if (x < 0 || y < 0 || x > width - 1 || y > height - 1)
      {
        outRed[n * width + m] = 0;
        outGreen[n * width + m] = 0;
        outBlue[n * width + m] = 0;
        outAlpha[n * width + m] = 255;
      }

      /* else, assign the corresponding values in each channels of input image to output image. */
      else
      {
        outRed[n * width + m] = inRed[y * width + x];
        outGreen[n * width + m] = inGreen[y * width + x];
        outBlue[n * width + m] = inBlue[y * width + x];
        outAlpha[n * width + m] = inAlpha[y * width + x];
      }
    }
  }
  /* the function has no return value. */
  return;
}

/* nearestPixel - computes the inverse transform to find the closest pixel in the original image
 * INPUTS: pixelYtransform - row value in transformed image
 *         pixelXtransform - column value in transformed image
 *         transform - two dimensional array containing transform coefficients of matrix T and vector S
 *         width - width of the input and output image
 *         height - height of the input and output image
 * OUTPUTS: pixelY - pointer to row value in original image
 *	    pixelX - pointer to column value in original image
 * RETURN VALUES: none
 */
void nearestPixel(int pixelYTransform, int pixelXTransform, double transform[2][3],
              int *pixelY, int *pixelX, int width, int height)
{
  /* Write your function here. */
  double reverse[4];   /* the inverse matrix of T. */

  /* calculate in mathematics the value of each element in T's inverse matrix. */
  reverse[0] = transform[1][1] / (transform[0][0] * transform[1][1] - transform[0][1] * transform[1][0]);
  reverse[1] = -1 * transform[0][1] / (transform[0][0] * transform[1][1] - transform[0][1] * transform[1][0]);
  reverse[2] = -1 * transform[1][0] / (transform[0][0] * transform[1][1] - transform[0][1] * transform[1][0]);
  reverse[3] = transform[0][0] / (transform[0][0] * transform[1][1] - transform[0][1] * transform[1][0]);

  /* the corresponding coodinates in input image of the coodinates in transformed image. */
  double x = (pixelXTransform - (width - 1) / 2 - transform[0][2]) * reverse[0] + (pixelYTransform - (height - 1) / 2 - transform[1][2]) * reverse[1];
  double y = (pixelXTransform - (width - 1) / 2 - transform[0][2]) * reverse[2] + (pixelYTransform - (height - 1) / 2 - transform[1][2]) * reverse[3];

  /* assign these cooderinates in the output pointers. */
  * pixelX = int(round(x + (width - 1) / 2));
  * pixelY = int(round(y + (height - 1) / 2));
  
  /* the function has no return value. */
  return;
}