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
        public int Lenght => Parts.Count;

        public Snake(Point initPosition) => Parts = new LinkedList<Point>(new []{initPosition});

        public void AddPart() => Parts.AddLast(Point.Empty);

        public IEnumerable<Point> CutTail(Point tailPartPosition)
        {
            var part = Parts.Find(tailPartPosition);
            var parts = new List<Point>();
            while (part != null)
            {
                var nextPart = part.Next;
                yield return part.Value;
                Parts.Remove(part);
                part = nextPart;
            }
        }

        public void MoveAfterHead(Point newHeadPosition)
        {
            Head.Value = newHeadPosition;
            var part = Tail;
            while (part.Previous != null)
            {
                part.Value.Offset(part.Previous.Value);
                part = part.Previous;
            }
        }
    }
}