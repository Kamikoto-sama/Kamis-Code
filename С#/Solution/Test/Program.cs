using System;
using System.Globalization;

namespace Test
{
    internal class Program
    {
        public static void Main(string[] args)
        {
            Console.WriteLine(ShouldFire2(true, "Zombie", 10));
        }
        static bool ShouldFire2(bool enemyInFront, string enemyName, int robotHealth)
        {
            return enemyInFront && (enemyName == "boss") && (robotHealth >= 50);
        }
    }
}