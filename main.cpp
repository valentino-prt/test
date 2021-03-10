//#include <QtCore/QCoreApplication> // enlevé sous xcode

#include <math.h>
#include "stdio.h"
//const char chaine1[10]="123.456,\0";


const char chaine2[10]="789,\0";
const char chaine3[10]=",\0";
const char chaine1[100]="$GPRMC,154936.000,A,4338.6124,N,00126.7337,E,0.26,326.08,200113,,,A*60\r\n\0";
const char chaine4[200]="$GPRMC,154936.000,A,4338.6124,N,00126.7337,E,0.26,326.08,200113,,,A*60\r\n$GPRMC,154936.000,A,4338.6124,N,00126.7337,E,0.26,326.08,200113,,,A*60\r\n\0";

 struct gps_data {
    char valid ; //trame valide
    float time ; //champ time de la trame
    float lat ; //champ latitude de la trame
    float lon ; //champ longitude de la trame
    unsigned char received_checksum;
};

 unsigned char computed_checksum=0; // variable de calcul du checksum
 char parserState=0; //etat courant du parser
 unsigned char counter= 0;
 unsigned char dp_counter=0;
 #define SYNC 0
 #define HEADER 1
 #define TIME 2
 #define VALID 3
 #define LAT 4
 #define LAT_DIR 5
 #define LONG 6
 #define LONG_DIR 7
 #define IGNORE 8
 #define CHECKSUM 9
 char header[6]="GPRMC";
 gps_data gps_d; //structure de stockage de la trame


/////////////////////////////////////////////////////////////////////////////////////
char parseFloatField(char c, float * ptr_val, unsigned char * ptr_count, unsigned char * ptr_dp_count) 
//La fonction renvoie 0 tant que le décodage n'est pas terminé
//                    1 lorsque le décodage est terminé correctement
//                   -1 lorsque le décodage a échoué
{
if (c >= '0' && c <= '9') 
  {
  (*ptr_val) *= 10;
  (*ptr_val) += c - '0';
  (*ptr_count) = (*ptr_count) + 1;
  return 0;
  } 
else if (c == '.') 
  {
  (*ptr_count) = 0;
  (*ptr_dp_count) ++ ;
  return 0;
  } 
else if (c == ',') 
  {
  while ((*ptr_count) > 0 && (*ptr_dp_count) > 0)  // équiptr_valent à (*ptr_val) = (*ptr_val)/(10^*count)
    {
    (*ptr_val) = (*ptr_val) / 10;
    (*ptr_count) = (*ptr_count) - 1;
    }
  if((*ptr_dp_count) > 1) 
    return -1 ;
  (*ptr_count) = 0 ;
  (*ptr_dp_count) = 0 ;
  return 1;
  } 
else     // caractère non supporté dans un nombre
  {
  (*ptr_count) = 0; 
  return -1;
  }
}
/////////////////////////////////////////////////////////////////////////////////////
char parseGPS(char c, struct gps_data * ptr_gps_data) {
    char ret = 1;
    float val;
    switch (parserState) {
        case SYNC:
            counter = 0;
            if (c == '$') {
                ptr_gps_data->lat = 0; //maz de la structure de stockage de la trame
                ptr_gps_data->lon = 0;
                ptr_gps_data->time = 0;
                ptr_gps_data->valid = -1;
                ptr_gps_data->received_checksum = 0;
                computed_checksum = 0;
                parserState = HEADER; //evolution de l'etat
            }
            break;
            
        case HEADER:
            computed_checksum = computed_checksum ^ c; // a faire dans chaque etat jusqu'au caractere '*'
            // le calcul de la somme de controle est fait par le XOR -> ^
            if (c == header[counter]) {
                counter ++;
            }else if(c==',' && counter == 5) {
                parserState = TIME;
            }else{
                parserState = SYNC;
            }
            break;
            
        //A COMPLETER!!!!!!!!!!!!!!!
        case TIME:
            computed_checksum = computed_checksum ^ c; // a faire dans chaque etat jusqu'au caractere '*'
            ret = parseFloatField(c, &val, &counter, &dp_counter);
            ptr_gps_data->time = val;
            if (ret == 1){
              
                parserState = VALID;
            }else{
                parserState = SYNC;
            }
            counter = 0;
            dp_counter =0;
            break;
            
        case VALID:
            computed_checksum = computed_checksum ^ c; // a faire dans chaque etat jusqu'au caractere '*'
            
            if (c == 'A') {
                ret = 1;
            }
            
            if (ret == 1 && c == ','){
                parserState = LAT;
            }else{
                parserState = SYNC;
            }
            break;
            
        case LAT:
            computed_checksum = computed_checksum ^ c; // a faire dans chaque etat jusqu'au caractere '*'
            
            ret = parseFloatField(c, &val, &counter, &dp_counter);
            ptr_gps_data->lat = val;
            
            if (ret == 1){
                parserState = LAT_DIR;
               
            }else{
                parserState = SYNC;
            }
            dp_counter =0;
            counter = 0;
            break;
            
        case LAT_DIR:
            computed_checksum = computed_checksum ^ c; // a faire dans chaque etat jusqu'au caractere '*'
            if (c == 'S'){
                ptr_gps_data->lat = -ptr_gps_data->lat;
                parserState = LONG;
            }else if (c == ','){
                parserState = LONG;
            }else if (c == 'E'){
                NULL;
            }else{
                parserState = SYNC;
            }
            break;
            
        case LONG:
            computed_checksum = computed_checksum ^ c; // a faire dans chaque etat jusqu'au caractere '*'
            
            ret = parseFloatField(c, &val, &counter, &dp_counter);
            ptr_gps_data->lon = val;
            
            if (ret == 1) {
                parserState = LONG_DIR;

            }else{
                parserState = SYNC;
            }
            counter = 0;
            dp_counter = 0;
            break;
            
        case LONG_DIR:
            computed_checksum = computed_checksum ^ c; // a faire dans chaque etat jusqu'au caractere '*'
            ret = parseFloatField(c, &val, &counter, &dp_counter);
            if (ret == 1) {
                ptr_gps_data->lon = val;
                parserState = IGNORE;
            }else{
                parserState = SYNC;
            }
            
            
            break;
            
        case IGNORE:
            computed_checksum = computed_checksum ^ c; // a faire dans chaque etat jusqu'au caractere '*'
            parserState = CHECKSUM;
            break;
        default:
        parserState = SYNC;
        break;
    }
    return 0;
}
/////////////////////////////////////////////////////////////////////////////////////
int main(int argc, char *argv[])
{
    //a enlever peut etre
    int ret = 0;
    char c = 'l';
    ///
    //A COMPLETER!!!!!!!!!!!!!!!   
     
    while (ret==0)
    {
      //A COMPLETER!!!!!!!!!!!!!!!   
      ret=parseGPS( c, &gps_d) ;
        if (ret==1)
        {
            printf("Trame décodée \n");
            printf("lat: %f \n",gps_d.lat);
            printf("lon: %f \n",gps_d.lon);
            printf("time: %f \n",gps_d.time);
            printf("valid: %d \n",(int)gps_d.valid);
            printf("ck: %02x \n",gps_d.received_checksum);
          
        }
        else if (ret==-1)
        {
            printf("Trame non décodée \n");
        }
    }
  
}
