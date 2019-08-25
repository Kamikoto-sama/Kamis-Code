using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.Serialization.Json;
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

        public static void Main(string[] args)
        {
            var type = new A().GetType();
            var members = type.GetMembers(Flags)
                .Where(member => member.MemberType.In(MemberTypes.Event, MemberTypes.Field));
            foreach (var memberInfo in members)
                Console.WriteLine($"{memberInfo.Name}, {memberInfo.MemberType}");
        }
    }

    public class A
    {
        public int PublicProp { get; set; }
        private int PrivateProp { get; set; }
        private static int PrivateStaticProp { get; set; }
        public static int PublicStaticProp { get; set; }

        private event Action PrivateEvent;
        public event Action PublicEvent;
        public static event Action PublicStaticEvent;
        private static event Action PrivateStaticEvent;

        public int PublicField;
        private int PrivateField;
        public int PublicStaticField;
        private int PrivateStaticField;

        public A()
        {
        }

        static A()
        {
        }
        
        public void PublicM()
        {
        }

        private void PrivateM()
        {
        }

        public static void PublicStaticM()
        {
        }

        private static void PrivateStaticM()
        {
        }

        public void Check()
        {
            Console.WriteLine(PublicProp);
            Console.WriteLine(PrivateProp);
            Console.WriteLine(PublicStaticProp);
            Console.WriteLine(PrivateStaticProp);
            Console.WriteLine(PublicField);
            Console.WriteLine(PrivateField);
            Console.WriteLine(PublicStaticField);
            Console.WriteLine(PrivateStaticField);
        }
    }
}