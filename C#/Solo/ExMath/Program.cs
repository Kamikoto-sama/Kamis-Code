using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;

namespace ExMath
{
    internal class Program
    {
        public static void Main(string[] args)
        {
            var values1 = new double[,]
            {
                {1, 2}, 
                {3, 4},
                {5 , 6}
            };
            var values2 = new double[,]
            {
                {2, 0},
                {0, 2}
            };
            var matrix = new Matrix(values1);
            Console.WriteLine(matrix * new Matrix(values2));
        }

        public static bool Method(Matrix matrix)
        {
            return matrix != null;
        }
    }
}