#include <iostream>
#include <cmath>

int n = 2000000;

bool isPrime(int num)
{
    bool resultado = true;
    for (int i = 2; i <= sqrt(num); i++)
    {
        if (num % i == 0)
        {
            resultado = false;
            break;
        }
    }

    return resultado;
}

int main() {
    while (n > 2) {
        isPrime(n);
        n--;
    }
    return 0;
}