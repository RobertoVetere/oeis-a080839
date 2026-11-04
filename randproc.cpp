// Proceso aleatorio: construir el triangulo por diagonales; en cada casilla libre se lanza una moneda justa.
// F = numero de casillas libres. Teorema (Jensen): log2 a(n) >= E[F].
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <random>
#include <cmath>
typedef unsigned __int128 u128;
int main(int argc,char**argv){
  int N=atoi(argv[1]); int R=atoi(argv[2]); std::mt19937_64 rng(atoi(argv[3]));
  std::vector<double> sumF(N+1,0), sumF2(N+1,0);
  for(int r=0;r<R;r++){
    std::vector<u128> E(1,1); long F=0;
    for(int n=1;n<N;n++){
      int g=E.size(); std::vector<u128> Nw(g+1); Nw[0]=1;
      for(int h=0;h<g;h++){ u128 x=E[h], y=Nw[h];
        if(h==g-1){ Nw[h+1]=x+y; break; }
        if(y>0 && y<=x){ F++; Nw[h+1]=(rng()&1)? x-y : x+y; } else Nw[h+1]=x+y; }
      E.swap(Nw); sumF[n+1]+=F; sumF2[n+1]+=(double)F*F;
    }
  }
  for(int n : {14,20,30,40,60,80,100,120}) if(n<=N){ double m=sumF[n]/R, sd=sqrt(sumF2[n]/R-m*m);
    printf("n=%3d  E[F]=%9.2f (+-%.2f)  E[F]/(n^2/2)=%.4f  frente a log2 a(n)/(n^2/2) ~ %.4f\n",n,m,sd/sqrt(R),m/(n*n/2.0), 0.0); }
}
