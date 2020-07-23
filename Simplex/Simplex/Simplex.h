#pragma once

#include <vector>
#include <algorithm>

typedef double DOUBLE;
typedef std::vector<DOUBLE> VD;
typedef std::vector<VD> VVD;
typedef std::vector<int> VI;


class LPSolver 
{

private:

    int m, n;
    VI B, N;
    VVD D;

    void Pivot(int, int);

    bool Simplex(int);

public:

    DOUBLE Solve(VD&);

    LPSolver(const VVD&, const VD&, const VD&);
};

