using System;
using System.Collections.Generic;

namespace Graphs
{
    public class Graph
    {
        private List<Node> nodes;
        public Node this[int nodeIndex] => nodes[nodeIndex];

        public Graph(int nodesCount) => nodes = new List<Node>(nodesCount);

        public Graph() => nodes = new List<Node>();

        public void Connect(int nodeIndex1, int nodeIndex2)
        {
            if (nodeIndex1 >= nodes.Count || nodeIndex2 >= nodes.Count)
                throw new ArgumentException("There is no node with such index");
        }
    }
}