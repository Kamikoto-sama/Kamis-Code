using System;

namespace VirtualMachine.Core
{
    internal static class Utils
    {
        public static byte[] ReverseIf(this byte[] data, bool reverse)
        {
            if (reverse)
                Array.Reverse(data);
            return data;
        }
    }
}