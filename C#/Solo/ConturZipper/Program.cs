using System;

namespace ConturZipper
{
    internal class Program
    {
        public static void Main(string[] args)
        {
            var temp = @"12.222.17.217 - - [03/Feb/2003:03:08:13 +0100] ""GET /jettop.htm HTTP/1.1""";
            var target = @"12.222.17.217 - - [03/Feb/2003:03:08:14 +0100] ""GET /jetstart.htm HTTP/1.1""";
            var result = XZipper.CompressString(target, temp);
            Console.WriteLine(result);
        }
    }
}