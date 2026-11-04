// Enumera todas las sucesiones de Gilbreath crecientes de longitud n (filas como caminos)
// y mide, para cada casilla (i,k), si la eleccion de signo es "libre":
// R_i[k+1] = R_i[k] ± R_{i+1}[k], libre si R_{i+1}[k]>0 y R_i[k]>=R_{i+1}[k] (fila 0: nunca libre).
#include <cstdio>
#include <cstdlib>
#include <cstring>
int n; long long total=0; double freeC[20][20]; double val[20][4]; // val: hist de valores 0,1,2,>=3 por fila
int T[20][20]; // T[i][k], fila i longitud n-i
// construimos por diagonales: añadir termino k a la fila 0 => nueva diagonal
void rec(int k){ // ya hay k terminos (columnas 0..k-1 en fila 0); diag: T[i][k-1-i]
  if(k==n){ total++;
    for(int i=0;i<n;i++) for(int c=0;c+1<n-i;c++){ int x=T[i][c], y=T[i+1][c]; if(i>0 && y>0 && x>=y) freeC[i][c]+=1; }
    for(int i=0;i<n;i++) for(int c=0;c<n-i;c++){ int v=T[i][c]; val[i][v>3?3:v]+=1; }
    return; }
  // nueva diagonal: T[k][0]=1 (fila k), T[i][k-i] = T[i][k-1-i] ± T[i+1][k-1-i]
  // recorremos desde abajo: fila k (nueva, valor 1), fila k-1, ..., fila 0
  T[k][0]=1;
  // DFS sobre i de k-1 a 0

  // recursion interna
  void go(int,int);
  go(k-1,k);
}
void go(int i,int k){
  if(i<0){ rec(k+1); return; }
  int c=k-i; int x=T[i][c-1], y=T[i+1][c-1];
  if(i==0){ if(y>0){ T[0][c]=x+y; go(-1,k);} return; }
  T[i][c]=x+y; go(i-1,k);
  if(y>0 && x>=y){ T[i][c]=x-y; go(i-1,k); }
}
int main(int argc,char**argv){ n=atoi(argv[1]); T[0][0]=1; rec(1);
  printf("n=%d total=%lld\n",n,total);
  printf("fraccion de casillas libres por (fila i, posicion k):\n");
  for(int i=1;i<n-1;i++){ printf("i=%2d:",i); for(int c=0;c+1<n-i;c++) printf(" %.2f",freeC[i][c]/total); printf("\n"); }
  printf("valores por fila: P(0) P(1) P(2) P(>=3)\n");
  for(int i=0;i<n;i++){ double s=val[i][0]+val[i][1]+val[i][2]+val[i][3]; printf("i=%2d: %.3f %.3f %.3f %.3f\n",i,val[i][0]/s,val[i][1]/s,val[i][2]/s,val[i][3]/s);} }
