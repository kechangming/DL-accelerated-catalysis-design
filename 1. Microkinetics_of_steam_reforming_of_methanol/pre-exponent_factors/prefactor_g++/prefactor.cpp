#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include "prefactor.h"
#include<math.h>
/* This code is used to calculate the prefactor of elementary reactions. unit of time is sec, length is m, weight is relative atomic mass, energy is eV/atom, surface site density is /cm^2¡£
 *
 *the inputs are freq.dat type file.
 *Usage: prefactor freq_ini.dat freq_trans.dat  <temperature> <energy>  # Here, freq_ini.dat is the frequency file of reactant, freq_trans.dat is the frequency file of transition state, unit of temperature is K, <energy> is not available in this version.
 *example in freq.dat
 *
 * forth parameter indicates the mode of motion: 
 * 
 * 4 parameters in a row
 *-1 indicates mode along reaction coordination, 
 *> 0 indicates vibrational, the value is the mass of molecules
 * 
 * 5 parameters for rotational mode
 * forth parameter is the symmery of mode
 * fifth parameter is the rotational inertia
 *case 1£º
 *frequency cm^{-1} ... 2
 *case 2£º
 *frequency cm^{-1} ... 2 8.9
*/
int main(int argc,char *argv[])
{
	if (argc!=5&&argc!=6)
	{
		printf("Usage: prefactor <minus> <transi> <temperature> <energy>\n");
		return NULL;
	}
	double site=1;
	if(argc==6){site=atof(argv[5]);}
	int row=0,row1=0,j=0,k=0,symmetry1=0,symmetry2=0;
	double mass,rotation1[3]={1.0,1.0,1.0},rotation2[3]={1.0,1.0,1.0};
	double total_partifunc1,total_partifunc2;
	char *filename1;
	filename1=argv[1];
	char *filename2;
	filename2=argv[2];
	double temperature=atof(argv[3]);
	double energy=atof(argv[4])*96.15384E3;
	char temp[50],line[200];
	FILE * fp1=NULL,* fp2=NULL;
	row = CountRow(filename1);
	row1 = CountRow(filename2);
	if (!(row==row1))
	{
		return NULL;
	}
	double *frequency1=(double *)calloc(row,sizeof(double));
	double *partifunc1=(double *)calloc(row,sizeof(double));
	double *frequency2=(double *)calloc(row,sizeof(double));
	double *partifunc2=(double *)calloc(row,sizeof(double));
	int *image1=(int *)calloc(row,sizeof(int));
	int *image2=(int *)calloc(row,sizeof(int));
	if((fp1=fopen(filename1,"r"))==NULL)
	{
		printf("Usage prefactor.out <file1> <file2> \n");
		return NULL;
	}
	if((fp2=fopen(filename2,"r"))==NULL)
	{
		printf("this second file is not exist \n");
		return NULL;
	}
	if (!(IsTransi(filename2)))
	{
		printf("The second file must a transition state \n");
		return NULL;
	}
	for (int i=0;i<row;i++)
	{
		fgets(line,sizeof(line),fp1);
		partifunc1[i]=PartiFuncGet(line,temperature,site);
		if (IsRotation(line))
		{
			symmetry1=SymmetryGet(line);
			rotation1[j]=RotationInertiaGet(line);
			j++;
		}
		fgets(line,sizeof(line),fp2);
		partifunc2[i]=PartiFuncGet(line,temperature,site);
		if (IsRotation(line))
		{
			symmetry2=SymmetryGet(line);
			rotation2[k]=RotationInertiaGet(line);
			k++;
		}
	}
	//for (int i=0;i<row;i++)
	//{
	//	printf("%lf \n",partifunc1[i]);
	//}
	//printf("%lf %d %1.8e %d %d %lf %lf",partifunc1[1],symmetry1,rotation1[0],j,row,temperature,energy);
	total_partifunc1=TotalPartiFunc(partifunc1,symmetry1,rotation1,j,row,temperature);
	if (Is3dTranslation(filename1)){total_partifunc1=total_partifunc1*pow(sqrt(site),3);}
	//printf("%lf %d %1.8e %d %d %lf %lf",partifunc2[1],symmetry2,rotation2[0],j,row,temperature,energy);
	total_partifunc2=TotalPartiFunc(partifunc2,symmetry2,rotation2,k,row,temperature);
	if (Is3dTranslation(filename2)){total_partifunc2=total_partifunc2*pow(sqrt(site),3);}
	
	double prefactor=Kb*temperature/h*total_partifunc2/total_partifunc1;//*exp(-energy/R/temperature);
	printf("%1.8e\n",prefactor);
	free(frequency1);free(frequency2);free(image1);free(image2);free(partifunc1);free(partifunc2);
	fclose(fp1);fclose(fp2);
	return 0;
}
