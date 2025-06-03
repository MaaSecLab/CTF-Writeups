#include <stdio.h>

int max(int a, int b) {
    return a > b ? a : b;
}

int main() {
    int n;
    scanf("%d", &n);
    
    int dp0 = -1, dp1 = -1, dp2 = -1;
    
    for (int i = 0; i < n; i++) {
        int x;
        scanf("%d", &x);
        
        if (x == 0) {
            int new_val = 0;
            if (dp0 >= 0) new_val = max(new_val, dp0);
            if (dp1 >= 0) new_val = max(new_val, dp1 + 4);
            if (dp2 >= 0) new_val = max(new_val, dp2 + 1);
            dp0 = max(dp0, new_val);
        } else if (x == 1) {
            int new_val = 0;
            if (dp0 >= 0) new_val = max(new_val, dp0 + 2);
            if (dp1 >= 0) new_val = max(new_val, dp1);
            if (dp2 >= 0) new_val = max(new_val, dp2 + 6);
            dp1 = max(dp1, new_val);
        } else {
            int new_val = 0;
            if (dp0 >= 0) new_val = max(new_val, dp0 + 3);
            if (dp1 >= 0) new_val = max(new_val, dp1 + 5);
            if (dp2 >= 0) new_val = max(new_val, dp2);
            dp2 = max(dp2, new_val);
        }
    }
    
    int result = max(dp0, max(dp1, dp2));
    printf("%d\n", result);
    fflush(stdout);
    
    return 0;
}