using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.Serialization.Json;
using System.Threading;
using System.Threading.Tasks;
using UsefulExtensions;

namespace Test
{
    class Program
    {
        public const BindingFlags Flags = BindingFlags.Instance 
                                          | BindingFlags.Static 
                                          | BindingFlags.NonPublic
                                          | BindingFlags.Public;

        enum E
        {
	        A, B, C
        }
        
        public static void Main(string[] args)
        {
	        var bytes = new byte[] {00, 00, 00, 05};

	        foreach (var hexIn in bytes.Select(b => (int)b))
	        {
		        Console.WriteLine($"{hexIn:X2}");
	        }
        }

        private static void M(A a)
        {
	        
        }
    }

    public class A
    {
	    public string Value;

	    public static implicit operator A(string value) => new A {Value = value};
    }
}