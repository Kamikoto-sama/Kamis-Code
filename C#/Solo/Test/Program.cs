using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Linq;
using System.Reflection;
using System.Runtime.Serialization;
using System.Threading;
using System.Threading.Tasks;
using UsefulExtensions;

namespace Test
{
    internal class Program
    {
        
        public static void Main(string[] args)
        {
            var dict = new Dictionary<List<int>, int>();
            var list = new List<int>{1, 2, 3};
            dict.Add(list, 10);
            Console.WriteLine(dict[list]);
            list[1] = 0;
            Console.WriteLine(dict.ContainsKey(list));
        }

        private static T Create<T>(T tObj)
        {
            var type = typeof(T);
            var properties = type.GetProperties();
            foreach (var property in properties)
            {
                if (!property.PropertyType.IsClass) continue;
                var valueCtor = property.PropertyType.GetConstructor(new Type[0]);
                var value = valueCtor.Invoke(new object[0]);
                property.SetValue(tObj, value);
            }

            return tObj;
        }
    }

    sealed class T_T
    {
        public int Count { get; set; }
        public List<int> List { get; set; }
    }
}