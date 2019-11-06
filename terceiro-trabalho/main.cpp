#include <iostream>

bool ehPrimo(int n) {
    int resultado = 0;
    for (int i = 2; i <= n / 2; i++) {
        if (n % i == 0) {
            resultado++;
        }
    }
    return resultado == 0;
}

int main() {
    int n = 10;

    for (int i = 1; i <= n; i++) {
        if (ehPrimo(i)) {
            std::cout << "Primo!";
        } else {
            std::cout << "Não!";
        }
    }

    return 0;
}