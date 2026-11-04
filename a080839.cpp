// a080839.cpp -- computes A080839(n): number of positive increasing integer sequences
// of length n whose Gilbreath transform is (1,1,1,...).
//
// Method (column-wise transfer on the absolute-difference triangle):
//   Write the triangle with rows i = 0..n-1 (row 0 = the sequence) and columns j.
//   Column 0 is (1,...,1). Since x(i+1,j) = |x(i,j+1) - x(i,j)|, column j+1 is obtained
//   from column j by x(i,j+1) = x(i,j) +- x(i+1,j), with every entry >= 0.
//   Row 0 must increase, so it always takes '+' and needs x(1,j) > 0.
//   The top entry of a column never influences later columns, so the state is the column
//   without its top entry. A state s of length m has children s'_i = s_i +- s_{i+1}
//   (i = 0..m-2, all entries >= 0), and it is alive only if s_0 > 0. The answer is the
//   number of paths from the initial state (1,...,1) of length n-1 down to length 0.
//   Identical states are merged with a hash table down to level K. Below K the
//   completions are counted by DFS, with closed forms for m <= 3 and a direct-mapped
//   cache (exact keys) for 5 <= m <= 8.
//
// Usage: ./a080839 n [P p]   -> splits the level-K states into P chunks and computes
//                              chunk p (the sum over p = 0..P-1 is a(n)). Default P=1.
// Build: g++ -O3 -march=native -o a080839 a080839.cpp
// Results: a(1..13) agree with the OEIS; a(14) = 5256046698145 (P=8, about 4 CPU-hours).
#include <cstdio>
#include <cstdlib>
typedef unsigned long long u64; typedef unsigned __int128 u128;

static int N;
static inline u64 pack(const int* s,int m,int bits){u64 k=0;for(int i=0;i<m;i++)k=(k<<bits)|(u64)s[i];return k;}
static inline void unpack(u64 k,int* s,int m,int bits){u64 mask=(1ULL<<bits)-1;for(int i=m-1;i>=0;i--){s[i]=k&mask;k>>=bits;}}
static inline u64 H(u64 x){x^=x>>33;x*=0xff51afd7ed558ccdULL;x^=x>>33;x*=0xc4ceb9fe1a85ec53ULL;x^=x>>33;return x;}

// closed forms for short states
static inline u64 f2(int a,int b){ return a<=0?0:1+((b>0&&a>b)?1:0); }
static inline u64 f3(int a,int b,int c){
  if(a<=0) return 0;
  u64 t=f2(a+b,b+c); if(c>0&&b>=c) t+=f2(a+b,b-c);
  if(b>0&&a>b){ t+=f2(a-b,b+c); if(c>0&&b>=c) t+=f2(a-b,b-c); }
  return t; }

// cache: in the state of length m every value is <= 2^(N-1-m), so N-m bits are enough
static const int CBITS=27, CMIN=5, CMAX=8;
static u64 *CK,*CV;

static u64 f(const int* s,int m);
static u64 rec(const int* s,int m,int* c,int i){   // build child c of length m-1
  if(i==m-1) return f(c,m-1);
  int x=s[i],y=s[i+1]; u64 t=0;
  c[i]=x+y; if(!(i==0&&c[0]==0)) t+=rec(s,m,c,i+1);
  if(y>0&&x>=y){ c[i]=x-y; if(!(i==0&&c[0]==0)) t+=rec(s,m,c,i+1); }
  return t; }
static u64 f(const int* s,int m){                   // number of completions of state s
  if(m==0) return 1; if(s[0]<=0) return 0; if(m==1) return 1;
  if(m==2) return f2(s[0],s[1]); if(m==3) return f3(s[0],s[1],s[2]);
  int c[16];
  if(m>=CMIN&&m<=CMAX){
    int bb=N-m; u64 key=(u64)m; for(int i=0;i<m;i++) key=(key<<bb)|(u64)s[i];
    u64 h=H(key)&((1ULL<<CBITS)-1);
    if(CK[h]==key) return CV[h];
    u64 r=rec(s,m,c,0); CK[h]=key; CV[h]=r; return r; }
  return rec(s,m,c,0); }

// open-addressing hash table state -> multiplicity
struct HT{ u64*k;u64*v;size_t cap,n;
  void init(size_t c){cap=c;n=0;k=(u64*)calloc(cap,8);v=(u64*)calloc(cap,8);if(!k||!v){fprintf(stderr,"out of memory\n");exit(1);}}
  void freeit(){free(k);free(v);}
  void grow(){HT o=*this;init(cap*2);for(size_t i=0;i<o.cap;i++)if(o.k[i])add(o.k[i],o.v[i]);o.freeit();}
  inline void add(u64 key,u64 val){if(n*10>=cap*7)grow();size_t i=H(key)&(cap-1);while(k[i]&&k[i]!=key)i=(i+1)&(cap-1);if(!k[i]){k[i]=key;n++;}v[i]+=val;}};
static HT nxt;
static void gen(const int* s,int m,int* c,int i,u64 cnt,int nb){
  if(i==m-1){ nxt.add(pack(c,m-1,nb),cnt); return; }
  int x=s[i],y=s[i+1];
  c[i]=x+y; if(!(i==0&&c[0]==0)) gen(s,m,c,i+1,cnt,nb);
  if(y>0&&x>=y){ c[i]=x-y; if(!(i==0&&c[0]==0)) gen(s,m,c,i+1,cnt,nb); } }

static void print128(u128 x){ char b[64];int q=63;b[q]=0;if(!x)b[--q]='0';while(x){b[--q]='0'+(int)(x%10);x/=10;} printf("%s\n",b+q); }

int main(int argc,char**argv){
  if(argc<2){ fprintf(stderr,"usage: %s n [P p]\n",argv[0]); return 1; }
  N=atoi(argv[1]); int P=argc>3?atoi(argv[2]):1, p=argc>3?atoi(argv[3]):0;
  if(N<1||N>14){ fprintf(stderr,"1 <= n <= 14 (64-bit state packing)\n"); return 1; }
  if(N<=3){ print128(1); return 0; }
  CK=(u64*)calloc(1ULL<<CBITS,8); CV=(u64*)calloc(1ULL<<CBITS,8);
  int K=N-5; if(K<3) K=3;                           // last level kept in the hash table
  int m=N-1,j=0,s[16],c[16]; for(int i=0;i<m;i++) s[i]=1;
  HT cur; cur.init(16); cur.add(pack(s,m,1),1);
  while(m>K){
    nxt.init(1<<16);
    for(size_t t=0;t<cur.cap;t++) if(cur.k[t]){ unpack(cur.k[t],s,m,j+1); if(s[0]<=0) continue; gen(s,m,c,0,cur.v[t],j+2); }
    cur.freeit(); cur=nxt; m--; j++; }
  u128 tot=0; size_t idx=0;
  for(size_t t=0;t<cur.cap;t++) if(cur.k[t]){ if((idx++)%P!=(size_t)p) continue; unpack(cur.k[t],s,m,j+1); tot+=(u128)cur.v[t]*f(s,m); }
  print128(tot);
  return 0; }
