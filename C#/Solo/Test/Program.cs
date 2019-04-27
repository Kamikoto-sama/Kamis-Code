using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UsefulExtensions;

namespace Test
{
    internal class Program
    {
        public static void Main(string[] args)
        {
            new B().M();
        }
    }

    class A
    {
        public A()
        {
            Console.WriteLine("A");
        }

        public void M()
        {
            Console.WriteLine(this + "A");
        }
    }

    class B: A
    {
        public B()
        {
            Console.WriteLine("B");
            M();
        }

        public void M()
        {
            base.M();   
        }
    }
}