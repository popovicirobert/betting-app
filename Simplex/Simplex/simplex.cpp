#include <iostream>
#include <vector>
#include <algorithm>
#include <iomanip>
#include <cassert>
#include <string>


typedef double DOUBLE;
typedef std::vector <DOUBLE> VD;
typedef std::vector <VD> VVD;
typedef std::vector <int> VI;

const DOUBLE EPS = 1e-3;

struct LPSolver {
    int m, n;
    VI B, N;
    VVD D;

    LPSolver(const VVD& A, const VD& b, const VD& c) :
        m(b.size()), n(c.size()), N(n + 1), B(m), D(m + 2, VD(n + 2)) {
        for (int i = 0; i < m; i++) for (int j = 0; j < n; j++) D[i][j] = A[i][j];
        for (int i = 0; i < m; i++) { B[i] = n + i; D[i][n] = -1; D[i][n + 1] = b[i]; }
        for (int j = 0; j < n; j++) { N[j] = j; D[m][j] = -c[j]; }
        N[n] = -1; D[m + 1][n] = 1;
    }

    void Pivot(int r, int s) {
        DOUBLE inv = 1.0L / D[r][s];
        for (int i = 0; i < m + 2; i++) if (i != r && abs(D[i][s]) > EPS / 100)
            for (int j = 0; j < n + 2; j++) if (j != s)
                D[i][j] -= D[r][j] * D[i][s] * inv;
        for (int j = 0; j < n + 2; j++) if (j != s) D[r][j] *= inv;
        for (int i = 0; i < m + 2; i++) if (i != r) D[i][s] *= -inv;
        D[r][s] = inv;
        std::swap(B[r], N[s]);
    }

    bool Simplex(int phase) {
        int x = phase == 1 ? m + 1 : m;
        while (true) {
            int s = -1;
            for (int j = 0; j <= n; j++) {
                if (phase == 2 && N[j] == -1) continue;
                if (s == -1 || D[x][j] < D[x][s] || D[x][j] == D[x][s] && N[j] < N[s]) s = j;
            }
            if (D[x][s] > -EPS) return true;
            int r = -1;
            for (int i = 0; i < m; i++) {
                if (D[i][s] < EPS) continue;
                if (r == -1 || D[i][n + 1] / D[i][s] < D[r][n + 1] / D[r][s] ||
                    (D[i][n + 1] / D[i][s]) == (D[r][n + 1] / D[r][s]) && B[i] < B[r]) r = i;
            }
            if (r == -1) return false;
            Pivot(r, s);
        }
    }

    DOUBLE Solve(VD& x) {
        int r = 0;
        for (int i = 1; i < m; i++) if (D[i][n + 1] < D[r][n + 1]) r = i;
        if (D[r][n + 1] < -EPS) {
            Pivot(r, n);
            if (!Simplex(1) || D[m + 1][n + 1] < -EPS) return -std::numeric_limits<DOUBLE>::infinity();
            for (int i = 0; i < m; i++) if (B[i] == -1) {
                int s = -1;
                for (int j = 0; j <= n; j++)
                    if (s == -1 || D[i][j] < D[i][s] || D[i][j] == D[i][s] && N[j] < N[s]) s = j;
                Pivot(i, s);
            }
        }
        if (!Simplex(2)) return std::numeric_limits<DOUBLE>::infinity();
        x = VD(n);
        for (int i = 0; i < m; i++) if (B[i] < n) x[B[i]] = D[i][n + 1];
        return D[m][n + 1];
    }
};


int main(int argc, char** argv) 
{

    //     maximize     c^T x
    //     subject to   Ax <= b
    //                  x >= 0
    //
    // INPUT: A -- an m x n matrix
    //        b -- an m-dimensional vector
    //        c -- an n-dimensional vector
    //        x -- an n-dimensional vector
    //             where the optimal solution will be stored
    //
    // OUTPUT: value of the optimal solution (infinity if unbounded
    //         above, nan if infeasible)
    //
    // To use this code, create an LPSolver object with A, b, and c as
    // arguments.  Then, call Solve(x).

    std::vector<double> CT;

    if (argc == 1)
    {
        CT = { 2.3, 3.3, 3.97 };
    }
    else 
    {
        assert(argc == 4);

        for (int i = 1; i < 4; i++) {
            CT.push_back(std::stoi(argv[i]));
        }
    }
    

    VVD a = { {-CT[0] + 1, 1, 1},
              {1, -CT[1] + 1, 1},
              {1, 1, -CT[2] + 1},
              {-1, 0, 0},
              {0, -1, 0},
              {0, 0, -1},
              {1, 0, 0},
              {0, 1, 0},
              {0, 0, 1} 
            };

    VD b = { 0, 0, 0, -200, -200, -200, 500, 500, 500 };
    VD c = { CT[0] - 3, CT[1] - 3, CT[2] - 3 };

    LPSolver lp(a, b, c);
    VD x;

    double answer = lp.Solve(x);
    double sum = 0;
    for (auto it : x) {
        sum += it;
    }
    std::cout << sum << "\n";

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

    return 0;
}