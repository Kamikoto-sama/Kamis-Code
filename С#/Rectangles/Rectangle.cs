namespace Rectangles
{
    public class Rectangle
    {
        public readonly int Left, Top, Width, Height;

        public Rectangle(int left, int top, int width, int height)
        {
            Left = left;
            Top = top;
            Width = width;
            Height = height;
        }

        public int Bottom {get{return Top + Height;}}
        public int Right {get{return Left + Width;}}

        public override string ToString()
        {
            return string.Format("Left: {0}, Top: {1}, Width: {2}, Height: {3}", Left, Top, Width, Height);
        }
    }
}