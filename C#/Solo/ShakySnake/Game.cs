using System;
using System.Collections.Generic;
using System.Drawing;

namespace ShakySnake
{
    public enum CellState{Empty, SnakePart, Fruit}
    public enum GameEnd{Won, Failed}

    public class GameModel
    {
        private readonly Size FieldSize;
        private readonly CellState[,] Field;
        public readonly Snake Snake;
        public Point Fruit { get; private set; }
        private Point _moveDirection;
        private Point _nextMoveDirection;
        public Point MoveDirection
        {
            get => _moveDirection;
            set => _nextMoveDirection = value;
        }
        public int Score { get; private set; }
        public bool StopDebug;
        
        public event Action<Snake> SnakeMoved;
        public event Action<Snake> FruitEaten;
        public event Action<GameEnd> GameOver;
        public event Action<List<Point>> SnakeAteSelfPart;

        public GameModel(Size fieldSize, Point playerInitPosition)
        {
            Field = new CellState[fieldSize.Width, fieldSize.Height];
            FieldSize = fieldSize;
            var head = playerInitPosition;
            Snake = new Snake(playerInitPosition);
            Field[head.X, head.Y] = CellState.SnakePart;
            Fruit = new Point(-1 ,-1);
            MoveDirection = new Point(1, 0);
        }

        public void Update()
        {
            var value = _nextMoveDirection;
            if (value.X != 0 && value.X + _moveDirection.X != 0 ||
                value.Y != 0 && value.Y + _moveDirection.Y != 0)
                _moveDirection = value;   
            MoveSnake();
            if (Fruit == new Point(-1 ,-1))
                SpawnFruit();
        }
        
        void MoveSnake()
        {
            var newHeadPosition = Snake.Head.Value + (Size) MoveDirection;
            newHeadPosition = MakeInBounds(newHeadPosition.X, newHeadPosition.Y);
            var headCellState = Field[newHeadPosition.X, newHeadPosition.Y];
            Field[newHeadPosition.X, newHeadPosition.Y] = CellState.SnakePart;
            var snakeTail = Snake.Tail.Value;
            if (Field[snakeTail.X, snakeTail.Y] != CellState.Fruit)
                Field[snakeTail.X, snakeTail.Y] = CellState.Empty;    
            switch (headCellState)
            {
                case CellState.SnakePart:
                    SnakeEatSelfPart(newHeadPosition);
                    break;
                case CellState.Fruit:
                    EatFruit(newHeadPosition);                
                    break;
            }
            Snake.MoveAfterHead(newHeadPosition);
            SnakeMoved?.Invoke(Snake);
        }

        void EatFruit(Point position)
        {
            Fruit = new Point(-1, -1);
            Score++;
            Snake.AddPart();
            FruitEaten?.Invoke(Snake);
        }

        void SnakeEatSelfPart(Point partPosition)
        {
            var eatenParts = Snake.CutTail(partPosition);
            foreach (var part in eatenParts)
            {
                if (Field[part.X, part.Y] == CellState.SnakePart)
                    Field[part.X, part.Y] = CellState.Empty;
            }
            SnakeAteSelfPart?.Invoke(eatenParts);
            if (eatenParts.Count > Snake.Length / 2)
                GameOver?.Invoke(GameEnd.Failed);
            Score = Snake.Length - 1;
        }

        void SpawnFruit()
        {
            var invokeCount = 0;
            while (invokeCount < FieldSize.Width * FieldSize.Height)
            {
                var rndGenerator = new Random();
                var xPos = rndGenerator.Next(0, FieldSize.Width);
                var yPos = rndGenerator.Next(0, FieldSize.Height);
                if (Field[xPos, yPos] is CellState.Empty)
                {
                    Field[xPos, yPos] = CellState.Fruit;
                    Fruit = new Point(xPos, yPos);
                    break;
                }
                invokeCount++;
            }
        }

        Point MakeInBounds(int x, int y) =>
            x < 0 ? new Point(FieldSize.Width - 1, y) :
            x >= FieldSize.Width ? new Point(0, y) :
            y < 0 ? new Point(x, FieldSize.Height - 1) :
            y >= FieldSize.Height ? new Point(x, 0) : new Point(x, y);
    }
}