using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Windows.Forms;
using System.Linq;
using System.Reflection;

namespace ShakySnake
{
    public class SnakeModel
    {
        public readonly List<Point> Parts;
        public Point Head;

        public SnakeModel(Point initPosition)
        {
            var head = initPosition;
            Head = head;
            Parts = new List<Point>{head};
        }

        public void Move(Direction direction, int step)
        {
            var xShift = 0;
            var yShift = 0;
            
            switch (direction)
            {
                case Direction.Up:
                    yShift = -step;
                    break;
                case Direction.Right:
                    xShift = step;
                    break;
                case Direction.Down:
                    yShift = step;
                    break;
                case Direction.Left:
                    xShift = -step;
                    break;
            }
            Head.Offset(xShift, yShift);
            for (var i = 1; i < Parts.Count; i++)
                Parts[i].Offset(Parts[i - 1]);
        }
    }

    public class SnakeView
    {
        public SnakeModel Model;
        public List<PictureBox> Parts;
        public PictureBox Head;

        public SnakeView(SnakeModel model)
        {
            Model = model;
            var head = new PictureBox();
        }
    }
}