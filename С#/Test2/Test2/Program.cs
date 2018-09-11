using System;
namespace Slide01
{
    class Program
    {
        static void Main()
        {
            System.Console.WriteLine(Min(4, 2, 3));
        }

        private static string GetMinX(int a, int b, int c)
        {
            if (a != 0)
            {
                double x0 = (-b) / (2.0 * a);
                return x0.ToString();
            }

            if (a == 0 && (c == 0 || c == 2))
            {
                return "a";
            }

            return "Impossible";
        }
    }
}