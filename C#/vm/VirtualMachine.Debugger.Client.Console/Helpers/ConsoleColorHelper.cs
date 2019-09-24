using System;

namespace VirtualMachine.Debugger.Client.Console.Helpers
{
    public static class ConsoleColorHelper
    {
        public static string ReadLine(this ConsoleColor color, string label = "")
        {
            color.Write(label + ":\t");
            return System.Console.ReadLine();
        }

        public static void WriteLine(this ConsoleColor color, string text = "") => color.Write($"{text}{Environment.NewLine}");

        public static void Write(this ConsoleColor color, string text)
        {
            lock (outputLock)
            {
                var old = System.Console.ForegroundColor;
                System.Console.ForegroundColor = color;
                System.Console.Write(text);
                System.Console.ForegroundColor = old;

            }
        }

        private static object outputLock = new object();
    }
}