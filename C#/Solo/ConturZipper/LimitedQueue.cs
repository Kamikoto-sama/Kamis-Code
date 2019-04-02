using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;

namespace ConturZipper
{
    public class LimitedQueue<T>: IEnumerable<T>
    {
        private Queue<T> Queue { get; }
        private int MaxSize { get; }
        public int Count => Queue.Count;

        public LimitedQueue(int maxSize)
        {
            Queue = new Queue<T>(maxSize);
            MaxSize = maxSize;
        }

        public void Add(T value)
        {
            Queue.Enqueue(value);
            if (Queue.Count > MaxSize)
                Queue.Dequeue();
        }

        public IEnumerator<T> GetEnumerator() => Queue.GetEnumerator();

        IEnumerator IEnumerable.GetEnumerator()
        {
            return GetEnumerator();
        }
    }
}