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
                {1, 3, 1}, 
                {3, 1, -4},
                {-1 , 4, 1}
            };
            var values2 = new double[,]
            {
                {2}
            };
            var matrix = new Matrix(values1);
            Console.WriteLine(matrix.Determinant);
//            Console.WriteLine(matrix
//                .Inverse
//                .Clone()
//                .Round(1)
//                .Transpose()
//                .GetMinor(0, 0)
//                .Rotate2D(Math.PI)
//                .SwapRows(0 ,1)
//                .RemoveRow(0)
//            );
        }

        public static bool Method(Matrix matrix)
        {
            return matrix != null;
        }
    }
}