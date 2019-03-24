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
            var values1 = new double[,]
            {
                {2, 3, 5, 7, 2}, 
                {2, 4, 3, 8, 5},
                {9 , 11, -13, 15, 1},
                {10, 1, 9, 16, 7},
                {4, 2, 3, 1, 11}
            };
            var values2 = new double[,]
            {
                {2}
            };
            var matrix = new Matrix(values2);
            Console.WriteLine(matrix.Determinant);
        }

        public static bool Method(Matrix matrix)
        {
            return matrix != null;
        }
    }
}