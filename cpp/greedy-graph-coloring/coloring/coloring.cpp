//#include <bits/stdc++.h>
#include <iostream>
#include <vector>
using namespace std;
vector<int> adj[101];
int main() {
  int n, m, i;
  cin >> n >> m;
  for (i = 1; i <= m; i++) {
    int u, v;
    cin >> u >> v;
    adj[u].push_back(v);
    adj[v].push_back(u);
  }
  int color[n + 1], available[n + 1], u, j;
  for (i = 0; i < n; i++) {
    color[i] = -1;
    available[i] = 0;
  }
  color[0] = 0;
  for (u = 1; u < n; u++) {
    for (j = 0; j < adj[u].size(); j++) {
      int to = adj[u][j];
      if (color[to] != -1)
        available[color[to]] = 1;
    }
    for (j = 0; j < n; j++)
      if (available[j] == 0)
        break;
    color[u] = j;
    for (j = 0; j < n; j++)
      available[j] = 0;
  }
  for (i = 0; i < n; i++)
    cout << color[i] << " ";
}
