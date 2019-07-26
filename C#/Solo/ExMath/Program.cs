using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Drawing.Drawing2D;

namespace ExMath
{
    internal class Program
    {
        public static void Main(string[] args)
        {
            Console.WriteLine(Combinatorics.Permutations(5) == 120);
            Console.WriteLine(Combinatorics.Permutations(10, 2, 3, 2) == 151200);
            Console.WriteLine(Combinatorics.Allocations(5, 3) == 5 * 4 * 3);
            Console.WriteLine(Combinatorics.Allocations(5, 5) == Combinatorics.Factorial(5));
            Console.WriteLine(Enumerable.Range(0, 6)
                .Aggregate(0,(x, y) => x + Combinatorics.Combinations(5, y)));
            Console.WriteLine(Combinatorics.CombinationsWithRep(3, 10) == 66);
        }

        public static bool Method(Matrix matrix)
        {
            return matrix != null;
        }
    }
}