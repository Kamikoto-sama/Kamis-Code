using System.Drawing;
using UsefulExtensions;

namespace ShakySnake
{
    enum CellState
    {
        Empty, SnakePart, Item
    }
    
    public class GameModel
    {
        private const int _step = 20;
        private readonly CellState[,] _field;
        private Point _head;
        
        public bool InFieldBounds(Point position, Size size)
        {
            return position.X >= 0 && position.Y >= 0 &&
                   position.X + size.Width <= _field. &&
                   position.Y + size.Height <= MainField.Height;
        }
    }
    
    
}