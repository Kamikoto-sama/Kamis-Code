using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using NUnit.Framework;

namespace ShakySnake
{
    public enum GameOverReason{AteTail, HeadBlown}

    public enum FieldObjects
    {
        Empty, SnakeHead, SnakePart, LostSnakeTail, Fruit, Chest, Key
    }
    
    public class GameModel
    {
        private const int MaxFruitCount = 5;
        private const int NewFruitProbability = 100;
        private const int MaxChestCount = 2;
        private const int NewChestProbability = 10;
        private const int NewKeyProbability = 5;
        private const int MaxProbabilityValue = 1000;
        private const int StepsToTailExplosion = 40;

        private int _leftStepsToTailExplosion = -1;
        private readonly FieldObjects[,] _field;
        private readonly Size _fieldSize;
        private Direction _moveDirection;
        private Direction _nextMoveDirection;
        private bool _keyExists;
        private bool _gameIsOver;
        private int _fruitsCount;
        private int _chestsCount;

        public Direction MoveDirection
        {
            get => _moveDirection;
            set => _nextMoveDirection = value;
        }
        public readonly Snake Snake;
        public List<Point> SnakeTail = new List<Point>();
        public int Score { get; private set; }
        public bool PlayerHasKey { get; private set; }

        public event Action<List<Point>, FieldObjects> ObjectsBlown;
        public event Action<Point, FieldObjects> ItemAppeared;
        public event Action<List<Point>> SnakeAteSelfPart;
        public event Action<GameOverReason> GameOver;
        public event Action<Point> SnakeCrashed;
        public event Action<Point> FruitEaten;
        public event Action<Snake> SnakeMoved;
        public event Action<Point> PlayerUsedKey;
        public event Action<Point> PlayerGotKey;

        public GameModel(Size fieldSize, Point playerInitPosition, 
            Direction initDirection)
        {
            _field = new FieldObjects[fieldSize.Width, fieldSize.Height];
            _fieldSize = fieldSize;
            Snake = new Snake(playerInitPosition);
            _field[playerInitPosition.X, playerInitPosition.Y] = FieldObjects.SnakeHead;

            MoveDirection = initDirection;
        }

        public void Update()
        {
            if (_gameIsOver) return;
            if (_leftStepsToTailExplosion == 0)
                MakeTailKaBoom();
            else
                _leftStepsToTailExplosion--;
            UpdateMoveDirection();
            MoveSnake();
            GenerateItems();
        }

        private void GenerateItems()
        {
            SpawnItem(FieldObjects.Fruit, NewFruitProbability, ref _fruitsCount, MaxFruitCount);
            SpawnItem(FieldObjects.Chest, NewChestProbability, ref _chestsCount, MaxChestCount);
            if (PlayerHasKey || _keyExists) return;
            var count = 0;
            _keyExists = SpawnItem(FieldObjects.Key, NewKeyProbability, ref count);
        }

        private void MakeGameOver(GameOverReason reason)
        {
            _gameIsOver = true;
            GameOver?.Invoke(reason);
        }
        
        private void MakeTailKaBoom()
        {
            var blownObjects = new List<Point>();
            foreach (var part in SnakeTail)
            {
                _field[part.X, part.Y] = FieldObjects.Empty;
                foreach (var cell in GetSurroundingCells(part))
                    if (BlowUpObject(MakeInBounds(cell.X, cell.Y)))
                        blownObjects.Add(cell);
            }
            if (_leftStepsToTailExplosion == 0) _leftStepsToTailExplosion = -1;
            ObjectsBlown?.Invoke(blownObjects, FieldObjects.LostSnakeTail);
        }

        private bool BlowUpObject(Point objPosition)
        {
            switch (_field[objPosition.X, objPosition.Y])
            {
                case FieldObjects.Fruit:
                    _field[objPosition.X, objPosition.Y] = FieldObjects.Empty;
                    _fruitsCount--;
                    return true;
                case FieldObjects.Chest:
                    TryOpenChest(objPosition, true);
                    return true;
                case FieldObjects.Key:
                    _field[objPosition.X, objPosition.Y] = FieldObjects.Empty;
                    _keyExists = false;
                    return true;
                case FieldObjects.SnakePart:
                    CutSnakeTail(objPosition, true);
                    return true;
                case FieldObjects.SnakeHead:
                    MakeGameOver(GameOverReason.HeadBlown);
                    return true;
            }
            return false;
        }
        
        private IEnumerable<Point> GetSurroundingCells(Point cell)
        {
            return new[]
            {
                new Point(cell.X, cell.Y + 1),
                new Point(cell.X - 1, cell.Y),
                new Point(cell.X + 1, cell.Y),
                new Point(cell.X, cell.Y - 1)
            }.Where(c => _field[c.X, c.Y] != FieldObjects.LostSnakeTail);
        }

        private void UpdateMoveDirection()
        {
            if ((int)_moveDirection + _nextMoveDirection != 0 && 
                _nextMoveDirection != Direction.None)
                _moveDirection = _nextMoveDirection;
        }

        private void MoveSnake()
        {
            var headPosition = Snake.Head.Value;
            var newHeadPosition = headPosition + DirectionToSize(_moveDirection);
            newHeadPosition = MakeInBounds(newHeadPosition.X, newHeadPosition.Y);
            var headCellState = _field[newHeadPosition.X, newHeadPosition.Y];
            
            var snakeCanMove = InteractWithFieldObject(newHeadPosition, headCellState);
            if (snakeCanMove)
            {
                _field[headPosition.X, headPosition.Y] = FieldObjects.SnakePart;
                _field[newHeadPosition.X, newHeadPosition.Y] = FieldObjects.SnakeHead;
                var snakeTail = Snake.Tail.Value;
                if (_field[snakeTail.X, snakeTail.Y] == FieldObjects.SnakePart)
                    _field[snakeTail.X, snakeTail.Y] = FieldObjects.Empty;
                Snake.MoveAfterHead(newHeadPosition);
                SnakeMoved?.Invoke(Snake);
            }
            else
            {
                MoveDirection = Direction.None;
//                SnakeCrashed?.Invoke(newHeadPosition);
            }
        }

        private Size DirectionToSize(Direction direction) =>
            direction == Direction.Up ? new Size(0, -1) :
            direction == Direction.Right ? new Size(1, 0) :
            direction == Direction.Down ? new Size(0, 1) :
            direction == Direction.Left ? new Size(-1, 0) :
            Size.Empty;

        private Point MakeInBounds(int x, int y) =>
            x < 0 ? new Point(_fieldSize.Width - 1, y) :
            x >= _fieldSize.Width ? new Point(0, y) :
            y < 0 ? new Point(x, _fieldSize.Height - 1) :
            y >= _fieldSize.Height ? new Point(x, 0) : new Point(x, y);

        private bool InteractWithFieldObject(Point objPosition, FieldObjects objType)
        {
            switch (objType)
            {
                case FieldObjects.SnakePart:
                    CutSnakeTail(objPosition);
                    break;
                case FieldObjects.Fruit:
                    EatFruit(objPosition);                
                    break;
                case FieldObjects.Chest:
                    return TryOpenChest(objPosition);
                case FieldObjects.LostSnakeTail:
                    return false;
                case FieldObjects.SnakeHead:
                    throw new Exception("You've crashed with your head :(");
                case FieldObjects.Key:
                    TakeKey(objPosition);
                    return true;
            }
            return true;
        }

        private void TakeKey(Point keyPosition)
        {
            PlayerHasKey = true;
            _keyExists = false;
            _field[keyPosition.X, keyPosition.Y] = FieldObjects.Empty;
            PlayerGotKey?.Invoke(keyPosition);
        }

        private bool TryOpenChest(Point chestPosition, bool byExplosion = false)
        {
            if (PlayerHasKey)
            {
                Score += 5;
                PlayerHasKey = false;
                _chestsCount--;
                PlayerUsedKey?.Invoke(chestPosition);
                return true;
            }
            if (byExplosion)
            {
                return true;
            }
            return false;
        }

        private void EatFruit(Point fruitPosition)
        {
            _fruitsCount--;
            Score++;
            Snake.AddPart();
            FruitEaten?.Invoke(fruitPosition);
        }

        private void CutSnakeTail(Point partPosition, bool byExplosion = false)
        {
            var eatenParts = Snake.CutTail(partPosition);
            foreach (var part in eatenParts)
                if (_field[part.X, part.Y] == FieldObjects.SnakePart)
                    _field[part.X, part.Y] = FieldObjects.LostSnakeTail;

            Score -= eatenParts.Count + 1;
            _leftStepsToTailExplosion = StepsToTailExplosion;
            SnakeTail = eatenParts;
            if (!byExplosion)
                SnakeAteSelfPart?.Invoke(eatenParts);
        }

        private bool SpawnItem(FieldObjects itemType , int probability, ref int count,
            int maxItemCount = 1)
        {
            var randomGenerator = new Random();
            var spawnItem = randomGenerator.Next(MaxProbabilityValue);

            if (spawnItem < MaxProbabilityValue - probability || count == maxItemCount)
                return false;
            var fieldArea = _fieldSize.Width * _fieldSize.Height;
            for (var i = 0; i < fieldArea; i++)
            {
                var xPos = randomGenerator.Next(0, _fieldSize.Width);
                var yPos = randomGenerator.Next(0, _fieldSize.Height);
                if (_field[xPos, yPos] != FieldObjects.Empty) continue;

                _field[xPos, yPos] = itemType;
                var position = new Point(xPos, yPos);
                count++;
                ItemAppeared?.Invoke(position, itemType);
                return true;
            }
            return false;
        }
    }
}