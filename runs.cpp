// Proceso controlado: moneda solo en descensos cuyo vecino izquierdo es ascenso (inicio de racha); '+' en los demas.
// Mide densidad de rachas (= monedas por posicion y nivel) y densidad de descensos. Contorno periodico.
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <random>
typedef long double ld;
int main(int argc,char**argv){
  int L=atoi(argv[1]), H=atoi(argv[2]); std::mt19937_64 rng(atoi(argv[3]));
  std::vector<ld> x(L), y(L);
  for(int g=0;g<L;g++) x[g]=1+(rng()%1000)/1000.0L;
  for(int h=0;h<=H;h++){
    std::vector<char> d(L);
    for(int g=0;g<L;g++){ ld a=x[(g+L-1)%L], b=x[g]; d[g]=(b>0 && b<=a); }
    int coins=0, desc=0;
    for(int g=0;g<L;g++){ int gm=(g+L-1)%L; ld a=x[gm], b=x[g]; int s=1;
      if(d[g]){ desc++; if(!d[gm]){ coins++; s=(rng()&1)?1:-1; } }
      y[g]=a+s*b; }
    ld mx=0; for(ld v:y) if(v>mx) mx=v; for(int g=0;g<L;g++) x[g]=y[g]/mx;
    if(h%(H/10)==0) printf("nivel %5d: monedas/pos %.4f  descensos %.4f\n",h,(double)coins/L,(double)desc/L);
  }
}
