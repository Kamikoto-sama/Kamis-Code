using System;
using System.Linq;
using System.Collections.Generic;
using System.Runtime.CompilerServices;

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

        public static int IndexOf<T>(this IEnumerable<T> array, T value)
        {
            var index = array
                .Select((e, i) => Tuple.Create(e, i))
                .FirstOrDefault(v => v.Item1.Equals(value));
            return index?.Item2 ?? -1;
        }

        public static int LastIndexOf<T>(this IEnumerable<T> array, T value)
        {
            var index = array
                .Select((e, i) => Tuple.Create(e, i))
                .LastOrDefault(v => v.Item1.Equals(value));
            return index?.Item2 ?? -1;
        }

        public static bool In<T>(this T value, ICollection<T> values) 
            => values.Contains(value);
    }
}