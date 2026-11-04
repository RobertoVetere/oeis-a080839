// Automata por niveles: x'_g = x_{g-1} + s_g x_g, s_g moneda justa si 0 < x_g <= x_{g-1} (descenso), si no '+'.
// Condicion de contorno periodica (g-1 de g=0 es el ultimo). Valores en long double, reescalados cada nivel.
#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <vector>
#include <random>
typedef long double ld;
int main(int argc,char**argv){
  int L=atoi(argv[1]), H=atoi(argv[2]); int mode=atoi(argv[3]); std::mt19937_64 rng(atoi(argv[4]));
  std::vector<ld> x(L), y(L);
  if(mode==0){ for(int g=0;g<L;g++) x[g]=1+(rng()%1000)/1000.0L; }            // aleatorio
  else { // mitad congelada (geometrica creciente, ratio 1+eps), mitad aleatoria; para periodicidad, la parte congelada
         // sube y luego hay una caida brusca
    ld eps=1e-3L; for(int g=0;g<L;g++){ if(g<L/2) x[g]=powl(1+eps,g); else x[g]=1+(rng()%1000)/1000.0L; } }
  for(int h=0;h<=H;h++){
    int desc=0, descL=0, descR=0;
    for(int g=0;g<L;g++){ ld a=x[(g+L-1)%L], b=x[g]; bool d=(b>0 && b<=a);
      if(d){desc++; if(g<L/2) descL++; else descR++;}
      y[g]= a + ((d && (rng()&1))? -b : b); }
    ld mx=0; for(ld v:y) if(v>mx) mx=v; for(int g=0;g<L;g++) x[g]=y[g]/mx;
    if(h%(H/10)==0) printf("nivel %5d: densidad descensos %.4f   (mitad izq %.4f, mitad der %.4f)\n",h,(double)desc/L,(double)descL/(L/2),(double)descR/(L/2));
  }
}
