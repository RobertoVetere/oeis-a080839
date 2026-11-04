// Busca implicaciones locales deterministas en el proceso aleatorio (diagonales).
// En la generacion g, nivel h: libre(g,h) <=> 0 < E'_h <= E_h. Eleccion c(g,h) in {'+','-','f'(forzado +)}.
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <random>
#include <map>
#include <string>
typedef unsigned __int128 u128;
int main(int argc,char**argv){
  int N=atoi(argv[1]), R=atoi(argv[2]); std::mt19937_64 rng(5);
  // estadisticas: patron (c(g,h), c(g-1,h)) -> (#casos, #libre en (g,h+1))
  std::map<std::string,std::pair<long,long>> st, st2;
  for(int r=0;r<R;r++){
    std::vector<u128> E(1,1); std::vector<char> prevc;
    for(int n=1;n<N;n++){
      int g=E.size(); std::vector<u128> Nw(g+1); Nw[0]=1; std::vector<char> c(g,'f'); std::vector<char> fr(g,0);
      for(int h=0;h<g;h++){ u128 x=E[h], y=Nw[h];
        if(h==g-1){ Nw[h+1]=x+y; c[h]='f'; break; }
        if(y>0 && y<=x){ fr[h]=1; if(rng()&1){Nw[h+1]=x-y;c[h]='-';} else {Nw[h+1]=x+y;c[h]='+';} } else { Nw[h+1]=x+y; c[h]='f'; } }
      if(n>20) for(int h=5;h+2<g-5;h++){
        std::string key; key+=c[h]; key+= (h<(int)prevc.size()? prevc[h]:'?');
        auto& p=st[key]; p.first++; p.second+=fr[h+1];
        std::string k2; k2+=c[h]; k2+=c[h+1];
        auto& q=st2[k2]; q.first++; q.second+= (h+2<g? fr[h+2]:0);
      }
      prevc=c; E.swap(Nw);
    }
  }
  printf("P(libre en (g,h+1) | c(g,h), c(g-1,h)):\n");
  for(auto& kv:st) printf("  %s : %.4f  (%ld)\n",kv.first.c_str(),(double)kv.second.second/kv.second.first,kv.second.first);
  printf("P(libre en (g,h+2) | c(g,h), c(g,h+1)):\n");
  for(auto& kv:st2) printf("  %s : %.4f  (%ld)\n",kv.first.c_str(),(double)kv.second.second/kv.second.first,kv.second.first);
}
