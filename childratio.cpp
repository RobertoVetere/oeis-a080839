// Para cada sucesion de Gilbreath P (longitud m), ext(P) = numero de extensiones crecientes validas,
// y rho(P) = (sum_{S hijo de P} ext(S)) / ext(P)^2. Se mide el minimo y la distribucion de rho por longitud.
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <cfloat>
#include <functional>
typedef long long ll;
int MAXL;
double minr[20]; ll cntN[20]; double sumlog[20]; ll below1[20];
// diagonal E (nivel 0 = abajo = 1 ... nivel m-1 = arriba = ultimo termino)
// genera todas las nuevas diagonales (extensiones crecientes)
#include <functional>
void kids(const std::vector<ll>& E, std::vector<std::vector<ll>>& out){
  int g=E.size(); std::vector<ll> N(g+1); N[0]=1;
  std::function<void(int)> rec=[&](int h){
    if(h==g-1){ if(N[h]>0){ N[h+1]=E[h]+N[h]; out.push_back(N);} return; }
    ll x=E[h], y=N[h];
    N[h+1]=x+y; rec(h+1);
    if(y>0 && y<=x){ N[h+1]=x-y; rec(h+1); }
  };
  rec(0);
}
// devuelve ext(P) y registra rho(P)
ll visit(const std::vector<ll>& E, int m){
  std::vector<std::vector<ll>> ch; kids(E,ch); ll e=ch.size();
  if(m>=MAXL) return e;
  ll s=0; for(auto& c:ch) s+=visit(c,m+1);
  if(e>0){ double r=(double)s/((double)e*e); if(r<minr[m]) minr[m]=r; cntN[m]++; sumlog[m]+=r; if(r<1.0) below1[m]++; }
  return e;
}
int main(int argc,char**argv){ MAXL=atoi(argv[1]); for(int i=0;i<20;i++) minr[i]=DBL_MAX;
  std::vector<ll> E(1,1); visit(E,1);
  for(int m=1;m<MAXL;m++) printf("longitud %d: P=%lld  min rho=%.4f  media rho=%.4f  casos rho<1: %lld\n",m,cntN[m],minr[m],sumlog[m]/cntN[m],below1[m]);
}
