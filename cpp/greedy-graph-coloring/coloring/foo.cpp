//#include <bits/stdc++.h>
#include <iostream>
#include <list>
#include <queue>
using namespace std;

class Graph {
public:
  int V;
  list<int> *adj;

  Graph(int v) {
    V = v;
    adj = new list<int>[V];
  }
  void addedge(int a, int b) {
    adj[a].push_back(b);
    adj[b].push_back(a);
  }

  void colors(int s) {
    bool *visited = new bool[V];
    int color[V];
    for (int i = 0; i < V; i++)
      color[i] = -1;
    color[s] = 0;
    queue<int> q;
    q.push(s);

    while (!q.empty()) {
      int f = q.front();
      q.pop();
      if (visited[f] == false) {
        visited[f] = true;
      }

      for (auto i : adj[f]) {
        if (visited[i] == false && color[i] == -1) {
          color[i] = 1 - color[f];
          q.push(i);
        }
        if (visited[i] == true && color[i] == color[f])
          color[f] = color[f] + 1;
      }
      cout << f << "--->" << color[f] << '\n';
    }
  }
};

int main() {
  int n, m, a, b;
  cin >> n >> m;
  Graph g(n);
  for (int i = 0; i < m; i++) {
    cin >> a >> b;
    g.addedge(a, b);
  }
  g.colors(0);

  return 0;
}
