#include<bits/stdc++.h>
using namespace std;

vector<int> divisors(int n) {
  vector<int> res;
  for (int i = 1; i * i <= n; ++i) {
    if(n % i == 0) {
      res.push_back(i);
      if(i != n / i)
        res.push_back(n / i);
    }
  }
  sort(res.begin(), res.end());
  return res;
}

bool isPrime(int n) {
  if (n < 2) return false;
  for (int i = 2; i * i <= n; ++i) {
    if (n % i == 0) return false;
  }
  return true;
}

vector<pair<int, int>> prime_factors(int n) {
  vector<pair<int, int>> res;
  for (int i = 1; i * i <= n; ++i) {
    int pow = 0;
    while(n % i) {
      n /= i, ++pow;
    }
    if (pow)
      res.push_back({i, pow});
  }
  if(n > 1)
    res.push_back({n, 1});

  return res;
}

vector<bool> sieve(int n) {
  vector<bool> prime(n + 1, true);
  prime[0] = prime[1] = false;
  for (int i = 2; i * i <= n; ++i){
    if(prime[i]) {
      for (int j = i * i; j <= n; j += i) {
        prime[j] = false;
      }
    }
  }
  return prime;
}

vector<int> spf(int n) {
  // Smallest Prime Factor (SPF)
  vector<int> spf(n + 1);
  for (int i = 0; i <= n; ++i)
    spf[i] = i;

  for (int i = 2; i * i <= n; ++i) {
    if(spf[i] == i) {
      for (int j = i * i; j <= n; j += i) {
        if (spf[j] == j) {
          spf[j] = i;
        }
      }
    }
  }
  return spf;
}

vector<int> count_prime_factors_from_spf(int N, vector<int>& spf) {
  vector<int> cnt(N + 1);
  for (int i = 2; i <= N; i++) {
    cnt[i] = cnt[i / spf[i]] + 1;
  }
  return cnt;
}
/*
  Applications of Prime Factorization
  -----------------------------------

  If:
  n = p1^a1 * p2^a2 * p3^a3 ...

  ---

  1. Number of Divisors

  Each prime p^a can appear in a divisor:
  0, 1, 2 ... a times

  So number of choices = a + 1

  Total number of divisors =
  (a1 + 1) * (a2 + 1) * (a3 + 1) ...

  Example:
  12 = 2^2 * 3^1

  Number of divisors =
  (2 + 1) * (1 + 1)
  = 3 * 2
  = 6

  Divisors:
  1 2 3 4 6 12

  ---

  2. Sum of Divisors

  For each prime, sum all possible powers.

  Example:
  12 = 2^2 * 3^1

  powers of 2:
  2^0 + 2^1 + 2^2
  = 1 + 2 + 4
  = 7

  powers of 3:
  3^0 + 3^1
  = 1 + 3
  = 4

  Sum of divisors =
  7 * 4
  = 28

  ---

  3. Generate All Divisors

  Take all possible powers of every prime
  then multiply every combination.

  Example:
  12 = 2^2 * 3^1

  powers of 2:
  1 2 4

  powers of 3:
  1 3

  combine them:

  1*1 = 1
  2*1 = 2
  4*1 = 4
  1*3 = 3
  2*3 = 6
  4*3 = 12

  All divisors:
  1 2 3 4 6 12

  ---

  4. GCD (Greatest Common Divisor)

  Take the common primes with the smallest power.

  Example:

  24 = 2^3 * 3^1
  36 = 2^2 * 3^2

  common primes:
  2 , 3

  smallest powers:
  2^2 , 3^1

  GCD =
  2^2 * 3^1
  = 4 * 3
  = 12

  ---

  5. LCM (Least Common Multiple)

  Take all primes with the largest power.

  Example:

  24 = 2^3 * 3^1
  36 = 2^2 * 3^2

  primes:
  2 , 3

  largest powers:
  2^3 , 3^2

  LCM =
  2^3 * 3^2
  = 8 * 9
  = 72

  gcd(a, b)  → product of min power
  lcm(a, b)  → product of max power
*/
/*
  to count how many number divisible by x in limit y
  → y / x
*/

int main() {
  int n;
  cin >> n;
}