using System.Collections;
using System.Collections.Generic;

namespace Test
{
    internal class Program
    {
        public static void Main(string[] args)
        {
        }
    }
    
    public class A<T>: ICollection<T>
    {
        private List<T> Values = new List<T>();

        public IEnumerator<T> GetEnumerator() => Values.GetEnumerator();

        IEnumerator IEnumerable.GetEnumerator()
        {
            return GetEnumerator();
        }

        public void Add(T item) => Values.Add(item);

        public void Clear() => Values.Clear();

        public bool Contains(T item) => Values.Contains(item);

        public void CopyTo(T[] array, int arrayIndex)
            => Values.CopyTo(array, arrayIndex);

        public bool Remove(T item) => Values.Remove(item);

        public int Count => Values.Count;
        public bool IsReadOnly => false;
        public int Value { get; set; }
    }
}