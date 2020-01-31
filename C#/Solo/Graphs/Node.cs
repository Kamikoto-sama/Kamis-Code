using System.Collections.Generic;

namespace Graphs
{
    public class Node
    {
        private static int newNodeIndex;

        public int Index;
        private List<Node> nodes;
        public Node this[int nodeIndex] => nodes[nodeIndex];

        public Node()
        {
            nodes = new List<Node>();
            Index = newNodeIndex++;
        }
    }
}