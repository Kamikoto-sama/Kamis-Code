using System;
using System.Globalization;

namespace Test
{
    internal class Program
    {
        public static void Main(string[] args)
        {
            var a = "10.0";
                double b = double.Parse(a, CultureInfo.InvariantCulture);
            Console.WriteLine(b);
        }
    }
}