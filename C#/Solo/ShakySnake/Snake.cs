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
        private readonly LinkedList<Point> _parts;
        public LinkedListNode<Point> Head => _parts.First;
        public LinkedListNode<Point> Tail => _parts.Last;
        public int Lenght => _parts.Count;

        public Snake(Point initPosition) => _parts = new LinkedList<Point>(new []{initPosition});

        public void AddPart() => _parts.AddLast(Point.Empty);

        public IEnumerable<Point> CutTail(Point tailPartPosition)
        {
            var part = _parts.Find(tailPartPosition);
            var parts = new List<Point>();
            while (part != null)
            {
                var nextPart = part.Next;
                yield return part.Value;
                _parts.Remove(part);
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