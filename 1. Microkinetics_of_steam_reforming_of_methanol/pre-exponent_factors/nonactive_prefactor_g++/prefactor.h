#include<stdio.h>
#include<stdlib.h>
#include<ctype.h>
#include<math.h>
#include<string.h>

#define h 6.62606896E-34    //the units if J*S
#define hbar 1.0545718E-34
#define Kb 1.3806488E-23      // J/K
#define Pi 3.1415926
#define H_mass 1.674E-27  //Kg
#define R 8.314              // J/mol/K

int CountRow(char * filename);  //count the row of a file
int CountElement(char *line);  //count the number of string of one line
char * ltrim(char *line);      //left trim space
char * rtrim(char *line);      //right trim space
double PartiFuncGet(char *line,double temperature,double site); //get the partitional function of one degree of freedom
int SymmetryGet(char *line); //get the symmetry of rotation from freq.dat file
double RotationInertiaGet(char *line); //get rotational inertia
int IsRotation(char *line); //Is a rotational mode on this degree of freedom?
double TotalPartiFunc(double *partifunc,int symmetry,double *rotation,int freedom,int row,double temperature);//calculation the total partitional function of a structure.
int IsTransi(char *filename); //Is a transition state? this freq.dat
int Is3dTranslation(char * filename); //Is there 3 dimensions translation this sturcture?
