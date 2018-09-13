using System;

namespace Test
{
    internal class Program
    {
        public static void Main(string[] args)
        {
            double v = double.Parse(Console.ReadLine());
            double d = double.Parse(Console.ReadLine());
            double a = Math.Asin(d * 9.8 / (v * v))/2;
            //a *= 180 / Math.PI;
            Console.WriteLine(Math.Round(a, 2));
        }
    }
}