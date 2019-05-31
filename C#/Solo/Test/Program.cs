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
        [Flags]
        public enum E
        {
            First = 0,
            Second = 1,
            Third = 2
        }
        
        public static void Main(string[] args)
        {
            var obj = Create(new T_T());
            Console.WriteLine(obj);
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

    class T_T
    {
        public int Count { get; set; }
        public List<int> List { get; set; }
    }
}