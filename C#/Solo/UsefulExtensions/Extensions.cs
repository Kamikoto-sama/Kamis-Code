using System;
using System.Collections.Generic;

namespace UsefulExtensions
{
    public static class Extensions
    {
        public static string Join<T>(this string separator, IEnumerable<T> values)
            => string.Join(separator, values);

        public static int ToInt(this string value)
        {
            int.TryParse(value, out var newValue);
            return newValue;
        }

        public static int ToInt(this double value) => (int) value;

        public static string ToPrint<T>(this IEnumerable<T> array)
            => "{" + ", ".Join(array) + "}";

        public static void Print(this string value) => Console.WriteLine(value);
        
        public static void Print<T>(this IEnumerable<T> array)
            => Console.WriteLine(array.ToPrint());
    }
}