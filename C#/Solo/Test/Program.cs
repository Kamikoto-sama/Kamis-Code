using System;
using System.Drawing;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UsefulExtensions;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Reflection;
using System.Runtime.InteropServices;

namespace Test
{
    internal class Program
    {
        enum State
        {
            Right, Left
        }
        
        public static void Main(string[] args)
        {
            var a = new State[2];
            Console.WriteLine(a[0]);
            Console.WriteLine(a[1]);
        }
    }

    partial class A
    {
        public int Count { get; set; }   
    }

    partial class A
    {
        public void M()
        {
            
        }
    }
}