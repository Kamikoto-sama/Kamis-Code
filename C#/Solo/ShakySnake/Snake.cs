using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Windows.Forms;
using System.Linq;
using System.Reflection;

namespace ShakySnake
{
    public class Snake
    {
        public readonly LinkedList<Point> Parts;
        public LinkedListNode<Point> Head => Parts.First;
        public LinkedListNode<Point> Tail => Parts.Last;
        public int Length => Parts.Count;

        public Snake(Point initPosition) 
            => Parts = new LinkedList<Point>(new []{initPosition});

        public void AddPart() => Parts.AddLast(Tail.Value);

        public List<Point> CutTail(Point tailPartPosition)
        {
            var part = Parts.Find(tailPartPosition);
            var parts = new List<Point>(Length);
            while (part != null)
            {
                var nextPart = part.Next;
                if (part.Value != tailPartPosition)
                    parts.Add(part.Value);
                Parts.Remove(part);
                part = nextPart;
            }
            return parts;
        }

        public void MoveAfterHead(Point newHeadPosition)
        {
            var part = Tail;
            while (part.Previous != null)
            {
                part.Value = part.Previous.Value;
                part = part.Previous;
            }
            Head.Value = newHeadPosition;
        }
    }
}