#include <iostream>

bool isPrime(int n) {
    int resultado = 0;
    for (int i = 2; i <= n/2; i++) {
        if (n % i == 0) {
            resultado++;
        }
    }
    
    return resultado == 0;
}

int main() {
    int n = 100000;

    for (int i = 1; i <= n; i++) {
        if (isPrime(i)) {
            // std::cout << i << ": Primo!" << std::endl;
        } else {
            // std::cout << i << ": Não!" << std::endl;
        }
    }

    return 0;
}