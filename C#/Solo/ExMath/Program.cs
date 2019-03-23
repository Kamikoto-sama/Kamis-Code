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
                {1, 1}, 
                {20, 20}
            };
            var values2 = new double[,]
            {
                {5, 2},
                {3, 6}
            };
            Console.WriteLine(new Matrix(values1) * new Matrix(values2));
        }
    }
}