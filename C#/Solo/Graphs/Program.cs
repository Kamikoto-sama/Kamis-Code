using System;

namespace Graphs
{
    internal class Program
    {
        public static void Main(string[] args)
        {
            var g = new Graph();
            Console.WriteLine(g[1][0][1]);
        }
    }
}