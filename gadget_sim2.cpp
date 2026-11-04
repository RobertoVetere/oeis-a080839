// Patrones periodicos de reglas (P,M,C) con monedas INDEPENDIENTES por posicion, sucesion larga ciclica.
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <random>
#include <string>
#include <cmath>
int main(){
  std::mt19937_64 rng(11); const int L=600, T=3000;
  const char* sym="PMC"; int found=0;
  for(int p=2;p<=7;p++){
    int tot=1; for(int i=0;i<p;i++) tot*=3;
    for(int code=0;code<tot;code++){
      std::string rule; int c=code; for(int i=0;i<p;i++){ rule+=sym[c%3]; c/=3; }
      if(rule.find('C')==std::string::npos) continue;
      int Lr=(L/p)*p; bool okany=false;
      for(int trial=0;trial<5 && !okany;trial++){
        std::vector<double> r(Lr), s(Lr), nr(Lr);
        std::uniform_real_distribution<double> U(0.05,0.95), U2(0.05,3.0);
        for(int g=0;g<Lr;g++) r[g]= (rule[g%p]=='P')? U2(rng):U(rng);
        bool ok=true;
        for(int t=0;t<T && ok;t++){
          for(int g=0;g<Lr;g++){ char q=rule[g%p]; if(q!='P' && !(r[g]>0 && r[g]<1)){ok=false;break;} if(r[g]<=0||!std::isfinite(r[g])){ok=false;break;}
            s[g]= q=='P'?1: q=='M'?-1: ((rng()&1)?1:-1); }
          if(!ok) break;
          for(int g=0;g<Lr;g++){ int h=(g+Lr-1)%Lr; nr[g]=r[h]*(1+s[g]*r[g])/(1+s[h]*r[h]); }
          r.swap(nr);
        }
        if(ok) okany=true;
      }
      if(okany){ found++; int cc=0; for(char ch:rule) cc+=(ch=='C'); printf("%s densidad %.3f\n",rule.c_str(),(double)cc/p); }
    }
  }
  printf("encontrados %d\n",found);
}
