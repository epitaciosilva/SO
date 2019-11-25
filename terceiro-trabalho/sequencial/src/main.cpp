#include <iostream>
#include <math.h>

bool isPrime(int n) {
    bool resultado = true;
    for (int i = 2; i <= sqrt(n); i++) {
        if (n % i == 0) {
            resultado = false;
            break;
        }
    }
    
    return resultado;
}

int main() {
    int n = 100000;
    int cont = 0;

    for (int i = 1; i <= n; i++) {
        if (isPrime(i)) {
            cont++;
        }
    }
    std::cout << cont << std::endl;

    return 0;
}