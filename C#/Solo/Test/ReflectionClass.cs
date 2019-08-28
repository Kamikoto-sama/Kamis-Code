using System;

namespace Test
{
    public class ReflectionClass
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

        public ReflectionClass()
        {
        }

        static ReflectionClass()
        {
        }
        
        public void PublicM(string a)
        {
            Console.WriteLine(a);
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