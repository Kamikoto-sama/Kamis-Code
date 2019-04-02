using System;
using System.IO;

namespace ConturZipper
{
    internal class Program
    {
        public static void Main(string[] args)
        {
            var log = File.ReadAllLines("../../log.txt");
            var result = XZipper.Compress(log);
            Console.WriteLine(result);
        }
    }
}