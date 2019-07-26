using System;
using System.Data;
using SQLiteAPI;
using UsefulExtensions;

namespace Test
{
    internal class Program
    {
        public static void Main(string[] args)
        {
            throw new Lol("HELLO");
        }
    }

    class Lol : Exception
    {
        public Lol(string message): base(message)
        {
        }

        public Lol()
        {
            
        }
    }
}