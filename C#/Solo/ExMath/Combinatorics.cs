using System.Linq;

namespace ExMath
{
    public static class Combinatorics
    {
        public static int Factorial(int value) 
            => Enumerable.Range(1, value).Aggregate(1, (i, j) => i * j);

        public static int Permutations(int elementsCount, params int[] repetitions) 
            => Factorial(elementsCount) / repetitions.Aggregate(1, (x, y) => x * Factorial(y));

        public static int Allocations(int n, int m) => n >= m ? Factorial(n) / Factorial(n - m) : 0;

        public static int Combinations(int n, int m) => n >= m ? Allocations(n, m) / Factorial(m) : 0;

        public static int CombinationsWithRep(int typesCount, int elementsCount) 
            => Combinations(typesCount - 1 + elementsCount, elementsCount);
    }
}