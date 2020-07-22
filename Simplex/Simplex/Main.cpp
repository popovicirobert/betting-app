#include <iostream>
#include <vector>
#include <algorithm>
#include <iomanip>
#include <cassert>
#include <string>

#include "Simplex.h"



int main(int argc, char** argv)
{

    std::vector<double> CT;
    double LIM;

    if (argc == 1)
    {
        CT = { 2.3, 3.3, 3.97 };
        LIM = 1000;
    }
    else
    {
        assert(argc == 4);

        for (int i = 1; i < 4; i++) {
            CT.push_back(std::stoi(argv[i]));
        }
        LIM = std::stoi(argv[4]);
    }


    std::vector<std::vector<double>> a = { {-CT[0] + 1, 1, 1},
                                            {1, -CT[1] + 1, 1},
                                            {1, 1, -CT[2] + 1},
                                            {1, 1, 1}
                                            };

    std::vector<double> b = { 0, 0, 0, LIM };
    std::vector<double> c = { CT[0] - 3, CT[1] - 3, CT[2] - 3 };

    LPSolver lp(a, b, c);
    std::vector<double> x;

    if (argc == 1)
    {
        double answer = lp.Solve(x);
        //double sum = 0;
        for (auto it : x) {
            //sum += it;
            std::cerr << it << "\n";
        }

        for (int i = 0; i < 3; i++)
        {
            double current = 0;
            for (int j = 0; j < 3; j++)
            {
                current += 1.0 * a[i][j] * x[j];
            }
            current *= -1;
            std::cout << std::fixed << std::setprecision(20) << current << "\n";
        }
        std::cin.get();
    }
    else
    {
        for (auto it : x) 
        {
            std::cout << it << " ";
        }
    }
    

    return 0;
}