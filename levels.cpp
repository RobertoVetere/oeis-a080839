// Densidad de casillas libres (= descensos) por nivel h en el proceso de monedas justas, triangulo de tamano N.
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <random>
typedef unsigned __int128 u128;
int main(int argc,char**argv){
  int N=atoi(argv[1]), R=atoi(argv[2]); std::mt19937_64 rng(9);
  std::vector<double> fr(N+1,0), tot(N+1,0);
  for(int r=0;r<R;r++){
    std::vector<u128> E(1,1);
    for(int n=1;n<N;n++){ int g=E.size(); std::vector<u128> Nw(g+1); Nw[0]=1;
      for(int h=0;h<g;h++){ u128 x=E[h], y=Nw[h];
        if(h==g-1){ Nw[h+1]=x+y; break; }
        tot[h]+=1;
        if(y>0 && y<=x){ fr[h]+=1; Nw[h+1]=(rng()&1)? x-y:x+y; } else Nw[h+1]=x+y; }
      E.swap(Nw); }
  }
  for(int h : {0,1,2,3,5,10,20,40,60,80,100,120,140,160,180}) if(h<N-1) printf("nivel %3d: densidad libre %.4f  (n_casillas=%.0f)\n",h,fr[h]/tot[h],tot[h]/R);
}
