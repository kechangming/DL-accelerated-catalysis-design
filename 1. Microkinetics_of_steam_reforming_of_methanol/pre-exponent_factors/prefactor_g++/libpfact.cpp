#include"prefactor.h"

/*===============================*/ //count the number of string of a line
int CountElement(char * line)
{
	int i=0,size_str=1;
	line=ltrim(rtrim(line));
	while(i<strlen(line))
	{
		if((line[i]==' ')&&(line[i+1]!=' '))size_str++;
		i++;
	}
	return size_str;
}

/*=============================*/ //count the row of a file
int CountRow(char *filename)
{
	int row=-1;
	char temp[100];
	FILE* fp=fopen(filename,"r");
while(!(feof(fp))){
	fgets(temp,sizeof(temp),fp);
	row++;
};
fclose(fp);
return row;
}

/*====================================*/ //trim left of a line
char *ltrim(char *line)
{
	while(isspace(*line))line++;
	return line;
}

/*==================================*/ //trim right of a line
char * rtrim (char *line)
{
	char *end = line+strlen(line)-1;
	while(end>line&& isspace(*end))
	{
		*end='\0';
		end--;
	}
	return line;
}

/*================================*/ //get the partitional function of one freedom
double PartiFuncGet(char *line,double temperature,double site)
{
	double frequency,partifunc=1.0,pre_constant=1.438776828;
	double mass;
	char temp[50];
	int image,imagenum=0;
	line=ltrim(rtrim(line));
	if (CountElement(line)==4)
	{
		sscanf(line,"%lf %s %s %d",&frequency,temp,temp,&image);
		//printf("%d\n",image);
		if (image==0)
		{partifunc=exp(-pre_constant*(frequency/temperature/2.0))/(1.0-exp(-pre_constant*(frequency/temperature)));}
		else if (image==-1)
		{
			partifunc=1.0;
			imagenum++;
			if(!(imagenum==1))
			{
				printf("every transis just have one imaginary frequency.");
				exit(0);
			}
		}
		else if (image>0)
		{
			mass=image*H_mass;
			partifunc=sqrt(2.0*Pi*mass*Kb*temperature)/(h*sqrt(site));
		}
		else {printf("the target is wrong \n");
		exit(0);}
	}
	else if (CountElement(line)==5)
	{
		sscanf(line,"%lf %s %s %d",&frequency,temp,temp,&image);
		if (image>0)
		{
			partifunc=1.0;
		}
		else {printf ("the symmetry of a system must greater than zero ");
		return NULL;}
	}
	else {printf("the element of this line is wrong!\n");
	return NULL;}
	return partifunc;
}

/*==================================*/ //get the symmetry of rotation from the file of freq.dat 
int SymmetryGet(char *line)
{
	char temp[50];
	int symmetry;
	line = ltrim(rtrim(line));
	sscanf(line,"%s %s %s %d",temp,temp,temp,&symmetry);
	if (symmetry<1)
	{
		printf("the symmetry of this system must be equal or greater than 1 \n");
		exit(0);
	}
	return symmetry;
}

/*========================================*/ //get rotational inertia 
double RotationInertiaGet(char *line)
{
	char temp[50];
	double rotation=0.0;
	sscanf(line,"%s %s %s %s %lf",temp,temp,temp,temp,&rotation);
	if (rotation<0.0&&CountElement(line)==5)
	{
		printf("the rotational inertia must greater than zero\n");
		exit(0);
	}
	return rotation*H_mass;
}

/*===================================*/ //Is a rotational mode on this degree freedom?
int IsRotation(char *line)
{
	char temp[50];
	int target;
	target=CountElement(line);
	if (target==5)return 1;
	else if(target==4)return 0;
	else {printf("the parameters of IsRptation is wrong \n");exit(0);}
}

int IsTransi(char * filename)
{
	int row=CountRow(filename),target=0,j=0;
	FILE *fp=fopen(filename,"r");
	char line[100];char temp[50];
	for (int i=0;i<row;i++)
	{
		fgets(line,sizeof(line),fp);
		sscanf(line,"%s %s %s %d",temp,temp,temp,&target);
		if (target==-1)
		{
			j++;
		}
	}
	fclose(fp);
	if (j==1){return 1;}
	return 0;
}

/*====================================*/ //calculation the total partitional function of a structure.
double TotalPartiFunc(double *partifunc,int symmetry,double * rotation,int freedom,int row,double temperature )
{
	double totalpartifunc=1.0;
	for(int i=0;i<row;i++)
	{
		totalpartifunc*=partifunc[i];
	}
	if (freedom==0)
	{
		printf("There is zero rotation \n");
		return totalpartifunc;
	}
	else if (freedom==1)
	{
		printf("There is one rotational freedom \n");
		totalpartifunc*=sqrt(2.0*Kb*temperature*Pi*rotation[0])/hbar/symmetry;
		return totalpartifunc;
	}
	else if (freedom==2)
	{
		printf("There is two rotational freedom \n");
		totalpartifunc*=2.0*Kb*temperature*rotation[0]/(hbar*hbar*symmetry);
		return totalpartifunc;
	}
	else if (freedom==3)
	{
		printf("There is three rotational freedom");
		totalpartifunc*=sqrt(Pi)*sqrt(pow(2*Kb*temperature/(hbar*hbar),3))*sqrt(rotation[0]*rotation[1]*rotation[2])/symmetry;
		return totalpartifunc;
	}
	else {
		printf("the freedom of rotation must between 0~3 \n");
		exit(0);
	}
}

int Is3dTranslation(char * filename)
{
	FILE*fp=NULL;
	char temp[50],line[200];
	int j=0,element;
	double mass=1.0;
	int row = CountRow(filename);
	if((fp = fopen(filename,"r"))==NULL){printf("the input of Is3dTranslation is wrong \n");exit(0);};
	for (int i=0;i<row;i++)
	{
		fgets(line,sizeof(line),fp);
		element=CountElement(line);
		sscanf(line,"%s %s %s %lf",temp,temp,temp,&mass);
		if (element==4&&mass>0.0)
		{
			j++;
		}
	}
	fclose(fp);
	if (j==3){printf("There are 3 translational degree of freedom \n");return 1;}
	else if (j==2){printf("There are 2 translational degree of freedom \n");return 0;}
	else if (j==1){printf("There is 1 translational degree of freedom \n");return 0;}
	else if (j==0){printf("There is no translational degree of freedom \n");return 0;}
	else {printf("freq.dat file is wrong \n");exit(-1);}
}
