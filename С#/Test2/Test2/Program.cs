using System;
namespace Slide01
{
    class Program
    {
        static void Main()
        {
            String a = Console.ReadLine();
            char[] s = a.ToCharArray();
            Array.Reverse(s);
        }
    }
}