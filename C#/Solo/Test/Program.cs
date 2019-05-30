using System;
using System.ComponentModel;
using System.Drawing;
using System.Threading;
using System.Threading.Tasks;

namespace Test
{
    internal class Program
    {
        public static void Main(string[] args)
        {
        }

        private static void DoWork(int time)
        {
            Console.WriteLine($"Thread{time} started");
            Thread.Sleep(time * 1000);
            Console.WriteLine("Thread" + time);
        }
        
    }
}