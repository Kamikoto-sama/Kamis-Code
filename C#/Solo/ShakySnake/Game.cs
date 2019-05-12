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
        public readonly Snake Snake;
        public Point MoveDirection;
        public int Score { get; private set; }
        public event Action ModelChanged;

        public GameModel(int fieldSize, Point playerInitPosition)
        {
            Field = new CellState[fieldSize, fieldSize];
            var head = playerInitPosition;
            Snake = new Snake(playerInitPosition);
            Field[head.X, head.Y] = CellState.SnakePart;
            MoveDirection = new Point(1, 0);
            SpawnFruit();
        }

        public void MoveSnake()
        {
            var newHeadPosition = Snake.Head.Value + (Size) MoveDirection;
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
            var snakeTail = Snake.Tail.Value;
            Field[snakeTail.X, snakeTail.Y] = CellState.Empty;
            Snake.MoveAfterHead(newHeadPosition);
        }

        void EatFruit(Point position)
        {
            Score++;
            Snake.AddPart();
        }

        void EatSnakeSelfPart(Point partPosition)
        {
            var snakeTail = Snake.CutTail(partPosition);
            foreach (var part in snakeTail)
                Field[part.X, part.Y] = CellState.Empty;
        }

        void SpawnFruit()
        {
            var rndGenerator = new Random();
            var xPos = rndGenerator.Next(0, FieldSize);
            var yPos = rndGenerator.Next(0, FieldSize);
            if (Field[xPos, yPos] is CellState.Empty)
                Field[xPos, yPos] = CellState.Fruit;
            else 
                SpawnFruit();
        }

        Point MakeInBounds(int x, int y) =>
            x < 0 ? new Point(FieldSize, y) :
            x >= FieldSize ? new Point(0, y) :
            y < 0 ? new Point(x, FieldSize) :
            y >= FieldSize ? new Point(x, 0) : new Point(x, y);
    }

    public class GameView
    {
        
    }
}