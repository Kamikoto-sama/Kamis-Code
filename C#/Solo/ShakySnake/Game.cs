using System;
using System.Collections.Generic;
using System.Drawing;
using System.Runtime.InteropServices;
using UsefulExtensions;

namespace ShakySnake
{
    public enum CellState{Empty, SnakePart, Fruit}

    public class GameModel
    {
        public int FieldSize => Field.GetLength(0);
        public readonly CellState[,] Field;
        private readonly Snake _snake;
        private Point _moveDirection;
        public Point MoveDirection
        {
            get => _moveDirection;
            set
            {
                if (value.X != 0 && value.X + _moveDirection.X != 0 ||
                    value.Y != 0 && value.Y + _moveDirection.Y != 0)
                    _moveDirection = value;
            }
        }
        public int Score { get; private set; }
        public event Action<Snake> SnakeMoved;
        public event Action<Snake> FruitEaten;
        public event Action<Point> FruitSpawned;

        public GameModel(int fieldSize, Point playerInitPosition)
        {
            Field = new CellState[fieldSize, fieldSize];
            var head = playerInitPosition;
            _snake = new Snake(playerInitPosition);
            Field[head.X, head.Y] = CellState.SnakePart;
            MoveDirection = new Point(1, 0);
            SpawnFruit();
        }

        public void MoveSnake()
        {
            var newHeadPosition = _snake.Head.Value + (Size) MoveDirection;
            newHeadPosition = MakeInBounds(newHeadPosition.X, newHeadPosition.Y);
            var headCellState = Field[newHeadPosition.X, newHeadPosition.Y];
            switch (headCellState)
            {
                case CellState.SnakePart:
                    EatSnakeSelfPart(newHeadPosition);
                    break;
                case CellState.Fruit:
                    EatFruit(newHeadPosition);                
                    break;
            }
            Field[newHeadPosition.X, newHeadPosition.Y] = CellState.SnakePart;
            var snakeTail = _snake.Tail.Value;
            Field[snakeTail.X, snakeTail.Y] = CellState.Empty;
            _snake.MoveAfterHead(newHeadPosition);
            SnakeMoved?.Invoke(_snake);
        }

        void EatFruit(Point position)
        {
            Score++;
            _snake.AddPart();
            FruitEaten?.Invoke(_snake);
        }

        void EatSnakeSelfPart(Point partPosition)
        {
            var snakeTail = _snake.CutTail(partPosition);
            foreach (var part in snakeTail)
                Field[part.X, part.Y] = CellState.Empty;
        }

        void SpawnFruit(int invokeCount = 0)
        {
            var rndGenerator = new Random();
            var xPos = rndGenerator.Next(0, FieldSize);
            var yPos = rndGenerator.Next(0, FieldSize);
            if (Field[xPos, yPos] is CellState.Empty)
            {
                Field[xPos, yPos] = CellState.Fruit;
                FruitSpawned?.Invoke(new Point(xPos, yPos));
            }
            else if (invokeCount < FieldSize)
                SpawnFruit(++invokeCount);
        }

        Point MakeInBounds(int x, int y) =>
            x < 0 ? new Point(FieldSize, y) :
            x >= FieldSize ? new Point(0, y) :
            y < 0 ? new Point(x, FieldSize) :
            y >= FieldSize ? new Point(x, 0) : new Point(x, y);
    }
}