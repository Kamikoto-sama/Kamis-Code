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
            var a = new[] {"hello", "my", "name"};
        }
    }

    class A
    {
        public virtual void M()
        {
            
        }
    }

    class B: A
    {
        public override void M()
        {
            base.M();
        }
    }
    
}