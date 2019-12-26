using System;
using System.Collections;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.ComponentModel;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.Serialization.Json;
using System.Threading;
using System.Threading.Tasks;
using Useful;

namespace Test
{
    class Program
    {
        public static void Main(string[] args)
        {
            M();
        }

        private static unsafe void M()
        {
            var a = "abc";
            var b = "abc";
            var x = &a;
            var y = &x;
            Console.WriteLine((uint) x);
        }
    }
}