/*
 * greedy algorithm for graph coloring
 *
 * */

#include <iostream>
#include <list>
#include <ostream>

// Undirected graph
class Graph {
  int V;               // No. of vertices
  std::list<int> *adj; // A dynamic array of adjacency lists
public:
  Graph(int V) {
    this->V = V;
    adj = new std::list<int>[V];
  }
  ~Graph() { delete[] adj; }

  int size() const { return V; }

  const std::list<int> *data() const { return adj; }

  void addEdge(int v, int w);

  void greedyColoring();
};

void Graph::addEdge(int v, int w) {
  adj[v].push_back(w);
  adj[w].push_back(v);
}

// Assigns colors (starting from 0) to all vertices
void Graph::greedyColoring() {
  int result[V];

  // Assign the first color to first vertex
  result[0] = 0;

  // Initialize remaining V-1 vertices as unassigned
  for (int u = 1; u < V; u++)
    result[u] = -1; // no color is assigned to u

  // A temporary array to store the available colors. True
  // value of available[cr] would mean that the color cr is
  // assigned to one of its adjacent vertices
  bool available[V];
  for (int cr = 0; cr < V; cr++)
    available[cr] = false;

  // Assign colors to remaining V-1 vertices
  for (int u = 1; u < V; u++) {
    // Process all adjacent vertices and flag their colors
    // as unavailable
    std::list<int>::iterator i;
    for (i = adj[u].begin(); i != adj[u].end(); ++i)
      if (result[*i] != -1)
        available[result[*i]] = true;

    // Find the first available color
    int cr;
    for (cr = 0; cr < V; cr++)
      if (available[cr] == false)
        break;

    result[u] = cr; // Assign the found color

    // Reset the values back to false for the next iteration
    for (i = adj[u].begin(); i != adj[u].end(); ++i)
      if (result[*i] != -1)
        available[result[*i]] = false;
  }

  // result dump
  std::cout << "Greedy graph coloring result dump:\n";
  for (int u = 0; u < V; u++)
    std::cout << "Vertex " << u << " ==> Color " << result[u] << '\n';
  std::cout << '\n';
}

std::ostream &operator<<(std::ostream &os, const Graph &g) {
  os << "Graph adjacency list dump:\n";
  const std::list<int> *_g = g.data();
  for (int i = 0; i < g.size(); ++i) {
    os << i << ": ";
    auto it = _g[i].begin(), ie = _g[i].end();
    for (; it != ie; ++it) {
      os << *it << " ";
    }
  os << '\n';
  }
  return os;
}

int main() {
  Graph g1(5);
  g1.addEdge(0, 1);
  g1.addEdge(0, 2);
  g1.addEdge(1, 2);
  g1.addEdge(1, 3);
  g1.addEdge(2, 3);
  g1.addEdge(3, 4);
  std::cout << g1;
  g1.greedyColoring();

  Graph g2(5);
  g2.addEdge(0, 1);
  g2.addEdge(0, 2);
  g2.addEdge(1, 2);
  g2.addEdge(1, 4);
  g2.addEdge(2, 4);
  g2.addEdge(4, 3);
  std::cout << g2;
  g2.greedyColoring();

  Graph g3(5);
  g3.addEdge(0, 4);
  g3.addEdge(0, 3);
  g3.addEdge(0, 2);
  g3.addEdge(0, 1);
  //g3.addEdge(1, 0);
  g3.addEdge(1, 3);
  //g3.addEdge(2, 0);
  g3.addEdge(2, 3);
  //g3.addEdge(3, 0);
  //g3.addEdge(3, 1);
  //g3.addEdge(3, 2);
  g3.addEdge(3, 4);
  //g3.addEdge(4, 0);
  //g3.addEdge(4, 3);
  std::cout << g3;
  g3.greedyColoring();

  Graph g4(6);
  g4.addEdge(0, 1);
  g4.addEdge(0, 2);
  g4.addEdge(0, 3);
  //g4.addEdge(1, 0);
  g4.addEdge(1, 4);
  //g4.addEdge(2, 0);
  g4.addEdge(2, 5);
  //g4.addEdge(3, 0);
  g4.addEdge(3, 4);
  //g4.addEdge(4, 1);
  //g4.addEdge(4, 3);
  g4.addEdge(4, 5);
  //g4.addEdge(5, 2);
  //g4.addEdge(5, 4);
  std::cout << g4;
  g4.greedyColoring();
  return 0;
}
