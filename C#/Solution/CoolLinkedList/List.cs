using System;
using System.Collections;
using System.Collections.Generic;
using System.Reflection.Emit;

namespace LinkedList
{
    public class CoolLinkedList<T>: IEnumerable<T>
    {
        private ListItem<T> Head { get; set; }
        private ListItem<T> Tail { get; set; }
        public int Count { get; private set; }

        public T this[int index]
        {
            get => GetItem(index).Value;
            set => GetItem(index).Value = value;
        }

        public IEnumerator<T> GetEnumerator()
        {
            var currentItem = Head;
            while (currentItem != null)
            {
                yield return currentItem.Value;
                currentItem = currentItem.Next;
            }
        }
        
        public void AddLast(T value)
        {
            Insert(Count, value);
        }

        public void Insert(int index, T value)
        {
            var newItem = new ListItem<T>(value);
            if (index < 0) index = Count + index;
            if(index >= Count + 1)
                throw new IndexOutOfRangeException();

            if (Head != null)
            {
                if(index < Count)
                {
                    var currentItem = GetItem(index);
                    newItem.Previous = currentItem.Previous;
                    newItem.Next = currentItem;
                    currentItem.Previous.Next = newItem;
                    currentItem.Previous = newItem;
                }
                else
                {
                    Tail.Next = newItem;
                    newItem.Previous = Tail;
                }
            }

            if (index == 0)
                Head = newItem;
            if (index == Count)
                Tail = newItem;
            Count++;
        }

        public ListItem<T> PopItem(int index)
        {
            var item = GetItem(index);
            if (index == 0)
                Head = Head.Next;
            if (index == Count - 1 && Head != null)
                Tail = Tail.Previous;
            Count--;
            return item;
        }

        public T Pop(int index)
        {
            return PopItem(index).Value;
        }

        public ListItem<T> GetItem(int index)
        {
            ListItem<T> item;
            if (index < 0) index = Count + index;
            if(index >= Count)
                throw new IndexOutOfRangeException();
            
            if (index + 1 <= Count / 2)
            {
                item = Head;
                for (var i = 0; i < index; i++)
                    item = item.Next;
            }
            else
            {
                item = Tail;
                for (var i = Count - 1; i < index; i--)
                    item = item.Previous;
            }

            return item;    
        }

        IEnumerator IEnumerable.GetEnumerator()
        {
            return GetEnumerator();
        }

        public override string ToString()
        {
            return "{" + string.Join(", ", this) + "}";
        }
    }

    public class ListItem<T>
    {
        public ListItem<T> Next { get; set; }
        public ListItem<T> Previous { get; set; }
        public T Value { get; set; }
        
        public ListItem(T value)
        {
            Value = value;
        }
    }
    
    public class Program
    {
        public static void Main(string[] args)
        {
            
        }
    }
}