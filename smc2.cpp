// SMC con remuestreo adaptativo a nivel de casilla (ESS < P/2) para log a(n), A080839.
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cmath>
#include <vector>
#include <random>
typedef unsigned __int128 u128;
int main(int argc,char**argv){
  int NMAX=atoi(argv[1]); int P=atoi(argv[2]); unsigned seed=argc>3?atoi(argv[3]):1;
  int S=NMAX+2;
  std::mt19937_64 rng(seed); std::uniform_real_distribution<double> U(0,1);
  std::vector<u128> O((size_t)P*S), N((size_t)P*S), O2((size_t)P*S), N2((size_t)P*S);
  std::vector<double> lw(P,0.0), wtmp(P); std::vector<int> pick(P);
  for(int p=0;p<P;p++) O[(size_t)p*S]=1;
  double logZ=0; printf("1 0\n");
  for(int n=1;n<NMAX;n++){ int g=n; // diagonal vieja: niveles 0..g-1
    for(int p=0;p<P;p++){ N[(size_t)p*S]=1; lw[p]=0; }
    for(int h=0;h<g;h++){
      for(int p=0;p<P;p++){ u128 x=O[(size_t)p*S+h], y=N[(size_t)p*S+h]; u128 r;
        if(h==g-1){ r=x+y; if(y==0) lw[p]=-INFINITY; }
        else if(y>0 && y<=x){ lw[p]+=M_LN2; r=(rng()&1)? x-y : x+y; }
        else r=x+y;
        N[(size_t)p*S+h+1]=r; }
      // ESS
      double mx=-INFINITY; for(double v:lw) if(v>mx) mx=v;
      double s=0,s2=0; for(int p=0;p<P;p++){ double w=std::exp(lw[p]-mx); wtmp[p]=w; s+=w; s2+=w*w; }
      double ess=s*s/s2;
      if(ess<P*0.5 || h==g-1){
        logZ += mx + std::log(s/P);
        double u=U(rng)*s/P, c=0; int j=0;
        for(int p=0;p<P;p++){ double t=u+(double)p*s/P; while(c+wtmp[j]<t && j<P-1){c+=wtmp[j];j++;} pick[p]=j; }
        for(int p=0;p<P;p++){ memcpy(&O2[(size_t)p*S],&O[(size_t)pick[p]*S],sizeof(u128)*(g+1)); memcpy(&N2[(size_t)p*S],&N[(size_t)pick[p]*S],sizeof(u128)*(h+2)); }
        O.swap(O2); N.swap(N2); for(int p=0;p<P;p++) lw[p]=0;
      }
    }
    O.swap(N);
    printf("%d %.6f\n",n+1,logZ); fflush(stdout);
  }
}
