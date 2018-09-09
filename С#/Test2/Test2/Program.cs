using System;

namespace Test2
{
    class Test
    {
        public static void Main()
        {
            var a = 10;
            var b = 20;
            a, b = b, a;
        }
    }
}