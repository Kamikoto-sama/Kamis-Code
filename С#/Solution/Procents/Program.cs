using System;
using System.Globalization;

namespace Procents
{
    internal class Program
    {
        public static void Main(string[] args)
        {
           string input = Console.ReadLine();
           Console.WriteLine(Calculate(input));
        }
        public static double Calculate(string userInput)
        {
            string[] data = userInput.Split(' ');
            double deposit = double.Parse(data[0], CultureInfo.InvariantCulture);
            double procent = double.Parse(data[1], CultureInfo.InvariantCulture);
            double month = double.Parse(data[2]);
            deposit = deposit * Math.Pow(1 + procent/100/ 12, month);
            return deposit;
        }
    }
}