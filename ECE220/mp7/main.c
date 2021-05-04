#include "imageData.h"
#include "functions.h"

const double gMonoMult[3]={.299,.587,.114};

int main(int argc,char *argv[])
{
  //Handles user input
  if(argc<4 || argc>5)
  {
    printf("Incorrect number of arguments\n");
    printf("Number of arguments: %d\n",argc);
    exit(1);
  }

  const char *inputFilename=argv[1];
  printf("Inputfile: %s\n",inputFilename);
  const char *outputFilename=argv[2];
  printf("Outputfile: %s\n",outputFilename);
  char garbage[2];
  int command;
  double sigma=3;

  double transform[2][3];

  if(1!=sscanf(argv[3],"%d%1s",&command,garbage) || command<0 || command>11)
  {
    printf("Incorrect command\n");
    exit(1);
  }

  if(command>0 && command<10 && argc==5)
  {
    printf("Incorrect number of arguments, exclude the sigma value\n");
    exit(1);
  }

  if(((command==0 || command==10) && argc==5 && 1!=sscanf(argv[4],"%lf%1s",&sigma,garbage)) || sigma<0)
  {
    printf("Incorrect sigma value\n");
    exit(1);
  }

  /*test for transform case, must include path to text file with transform matrix specified*/
  	
  if(command==11)
  {
	const char *transformFilename=argv[4];
  	printf("Transform file: %s\n",transformFilename);
	FILE *fp;

	if((fp = fopen(transformFilename,"r")))
	{
		int i = 0;
		size_t count;
		char *linestring = (char*)malloc(sizeof(char)*50); /*should be plenty if properly formatted*/
		for(i=0;i<2;i++){
			getline(&linestring,&count,fp);
			sscanf(linestring,"%lf %lf %lf", &transform[i][0],&transform[i][1],&transform[i][2]);
		}
		fclose(fp);
	}
	else
	{
		printf("No transform matrix file. \n");
		exit(1);
	}
	
  }

  Filter *filters=initializeFilters(sigma);
  Image *inputImage=decode(inputFilename);
  printf("Width: %d, height: %d\n",inputImage->width,inputImage->height);
  Image *outputImage=generateOutput(inputImage);

  uint8_t *inRed=inputImage->redChannel;
  uint8_t *inBlue=inputImage->blueChannel;
  uint8_t *inGreen=inputImage->greenChannel;
  uint8_t *inAlpha=inputImage->alphaChannel;
  uint8_t *outRed=outputImage->redChannel;
  uint8_t *outBlue=outputImage->blueChannel;
  uint8_t *outGreen=outputImage->greenChannel;
  uint8_t *outAlpha=outputImage->alphaChannel;
  int height=inputImage->height;
  int width=inputImage->width;
  switch(command)
  {
    case(0):
    {
      convolveImage(inRed,inGreen,inBlue,inAlpha,outRed,outGreen,outBlue,
                    outAlpha,filters[0].filter,filters[0].radius,width,height);
      break;
    }
    case(1):
    {
      convolveImage(inRed,inGreen,inBlue,inAlpha,outRed,outGreen,outBlue,
                    outAlpha,filters[1].filter,filters[1].radius,width,height);
      break;
    }
    case(2):
    {
      convolveImage(inRed,inGreen,inBlue,inAlpha,outRed,outGreen,outBlue,
                    outAlpha,filters[2].filter,filters[2].radius,width,height);
      break;
    }
    case(3):
    {
      convolveImage(inRed,inGreen,inBlue,inAlpha,outRed,outGreen,outBlue,
                    outAlpha,filters[3].filter,filters[3].radius,width,height);
      break;
    }
    case(4):
    {
      convolveImage(inRed,inGreen,inBlue,inAlpha,outRed,outGreen,outBlue,
                    outAlpha,filters[4].filter,filters[4].radius,width,height);
      break;
    }
    case(5):
    {
      convolveImage(inRed,inGreen,inBlue,inAlpha,outRed,outGreen,outBlue,
                    outAlpha,filters[5].filter,filters[5].radius,width,height);
      break;
    }
    case(6):
    {
      convolveImage(inRed,inGreen,inBlue,inAlpha,outRed,outGreen,outBlue,
                    outAlpha,filters[6].filter,filters[6].radius,width,height);
      break;
    }
    case(7):
    {
      convertToGray(inRed,inGreen,inBlue,inAlpha,outRed,outGreen,outBlue,
                    outAlpha,gMonoMult,width,height);
      break;
     }
    case(8):
    {
      invertImage(inRed,inGreen,inBlue,inAlpha,outRed,outGreen,outBlue,
                  outAlpha,width,height);
      break;
    }
    case(9):
    {
      pixelate(inRed,inGreen,inBlue,inAlpha,outRed,outGreen,outBlue,
               outAlpha,8,8,width,height);
      break;
    }
    case(10):
    {
      Image *invImage=generateOutput(inputImage);
      Image *blurImage=generateOutput(inputImage);
      pencilSketch(inRed,inGreen,inBlue,inAlpha,invImage->redChannel,
                   invImage->greenChannel,invImage->blueChannel,
                   invImage->alphaChannel,blurImage->redChannel,
                   blurImage->greenChannel,blurImage->blueChannel,
                   blurImage->alphaChannel,outRed,outGreen,outBlue,
                   outAlpha,filters[0].filter,filters[0].radius,width,
                   height,gMonoMult);
      freeImage(invImage);
      freeImage(blurImage);
      break;
    }
    case(11):
    {
      printf("Image Transformation\n");
      transformImage(inRed,inGreen,inBlue,inAlpha,outRed,outGreen,outBlue,outAlpha,transform,width,height);
      break;
    }
    default:
      exit(1);
  }

  encode(outputFilename,outputImage);

  free((double*)filters[0].filter);
  free(filters);
  freeImage(inputImage);
  freeImage(outputImage);
  return 0;
}
