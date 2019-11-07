#include <iostream>
#include <thread>
#include <mutex>

int n = 100000;

bool shared_n(int j){
    std::mutex mu;
    mu.lock();
    n -= j;
    mu.unlock();
    return n;
}

bool isPrime(int j) {
    int n = shared_n(j);
    int resultado = 0;
    for (int i = 2; i <= n/2; i++) {
        if (n % i == 0) {
            resultado++;
        }
    }
    
    return resultado == 0;
}

int main() {
    int t = 2;
    // for (int i = 1; i <= n; i++) {
        for(int j = 1; j <= t; j++){
            std::thread prime_thread(isPrime, j);
        }


        // if (isPrime(i)) {
        //     std::cout << i << ": Primo!" << std::endl;
        // } else {
        //     std::cout << i << ": Não!" << std::endl;
        // }
    // }

    return 0;
}