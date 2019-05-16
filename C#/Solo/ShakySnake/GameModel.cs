using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;

namespace ShakySnake
{
    public enum GameOverReason{AteTail, HeadBlown}
    public enum FieldObjects{Empty, SnakeHead, SnakePart, LostSnakeTail, Fruit, Chest, Key}
    
    public class GameModel
    {
        private const int MaxFruitCount = 6;
        private const int NewFruitProbability = 300;
        private const int MaxChestCount = 4;
        private const int NewChestProbability = 100;
        private const int NewKeyProbability = 50;
        private const int MaxProbabilityValue = 1000;
        private const int StepsToTailExplosion = 3;

        private int _leftStepsToTailExplosion = -1;
        private readonly FieldObjects[,] _field;
        private readonly Size _fieldSize;
        private Point _moveDirection;
        private Point _nextMoveDirection;
        private bool _keyExists;
        private bool _gameIsOver;

        public Point MoveDirection
        {
            get => _moveDirection;
            set => _nextMoveDirection = value;
        }
        public readonly Snake Snake;
        public List<Point> SnakeTail = new List<Point>();
        public int Score { get; private set; }
        public bool PlayerHasKey { get; private set; }
        public readonly HashSet<Point> Fruits;
        public readonly HashSet<Point> Chests;

        public event Action<List<Tuple<Point, FieldObjects>>> ObjectsBlown;
        public event Action<List<Point>> SnakeAteSelfPart;
        public event Action<GameOverReason> GameOver;
        public event Action<Point> SnakeCrashed;
        public event Action<Point> ChestOpened;
        public event Action<Point> FruitEaten;
        public event Action<Snake> SnakeMoved;
        public event Action PlayerUsedKey;
        public event Action PlayerGotKey;

        public GameModel(Size fieldSize, Point playerInitPosition, Point initDirection)
        {
            _field = new FieldObjects[fieldSize.Width, fieldSize.Height];
            _fieldSize = fieldSize;
            Snake = new Snake(playerInitPosition);
            _field[playerInitPosition.X, playerInitPosition.Y] = FieldObjects.SnakeHead;

            MoveDirection = initDirection;
            Fruits = new HashSet<Point>();
            Chests = new HashSet<Point>();
        }

        public void Update()
        {
            if (_gameIsOver) return;
            if (_leftStepsToTailExplosion == 0)
                MakeTailKaBoom();
            UpdateMoveDirection();
            MoveSnake();
            SpawnItem(FieldObjects.Fruit, NewFruitProbability, MaxFruitCount, Fruits);
            SpawnItem(FieldObjects.Chest, NewChestProbability, MaxChestCount, Chests);
            if (PlayerHasKey || _keyExists) return;
            _keyExists = SpawnItem(FieldObjects.Key, NewKeyProbability, itemState: _keyExists);
        }

        private void MakeGameOver(GameOverReason reason)
        {
            _gameIsOver = true;
            GameOver?.Invoke(reason);
        }
        
        private void MakeTailKaBoom()
        {
            var blownObjects = new List<Tuple<Point, FieldObjects>>();
            foreach (var part in SnakeTail)
            {
                _field[part.X, part.Y] = FieldObjects.Empty;
                foreach (var cell in GetSurroundingCells(part))
                    if (BlowUpObject(MakeInBounds(cell.X, cell.Y), out var obj))
                        blownObjects.Add(obj);
            }
            if (_leftStepsToTailExplosion == 0) _leftStepsToTailExplosion = -1;
            ObjectsBlown?.Invoke(blownObjects);
        }

        private bool BlowUpObject(Point objPosition, out Tuple<Point, FieldObjects> obj)
        {
            switch (_field[objPosition.X, objPosition.Y])
            {
                case FieldObjects.Fruit:
                    _field[objPosition.X, objPosition.Y] = FieldObjects.Empty;
                    Fruits.Remove(objPosition);
                    obj = Tuple.Create(objPosition, FieldObjects.Fruit);
                    return true;
                case FieldObjects.Chest:
                    TryOpenChest(objPosition, true);
                    obj = Tuple.Create(objPosition, FieldObjects.Chest);
                    return true;
                case FieldObjects.Key:
                    _field[objPosition.X, objPosition.Y] = FieldObjects.Empty;
                    _keyExists = false;
                    obj = Tuple.Create(objPosition, FieldObjects.Key);
                    return true;
                case FieldObjects.SnakePart:
                    CutSnakeTail(objPosition, true);
                    obj = Tuple.Create(objPosition, FieldObjects.SnakePart);
                    return true;
                case FieldObjects.SnakeHead:
                    MakeGameOver(GameOverReason.HeadBlown);
                    obj = Tuple.Create(objPosition, FieldObjects.SnakeHead);
                    return true;
            }
            obj = null;
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
            var value = _nextMoveDirection;
            if (value.X != 0 && value.X + _moveDirection.X != 0 ||
                value.Y != 0 && value.Y + _moveDirection.Y != 0)
                _moveDirection = value;
        }

        private void MoveSnake()
        {
            var newHeadPosition = Snake.Head.Value + (Size) MoveDirection;
            newHeadPosition = MakeInBounds(newHeadPosition.X, newHeadPosition.Y);
            var headCellState = _field[newHeadPosition.X, newHeadPosition.Y];
            
            var snakeCanMove = InteractWithFieldObject(newHeadPosition, headCellState);
            if (snakeCanMove)
            {
                _field[newHeadPosition.X, newHeadPosition.Y] = FieldObjects.SnakeHead;
                var snakeTail = Snake.Tail.Value;
                if (_field[snakeTail.X, snakeTail.Y] == FieldObjects.SnakePart)
                    _field[snakeTail.X, snakeTail.Y] = FieldObjects.Empty;
                Snake.MoveAfterHead(newHeadPosition);
                SnakeMoved?.Invoke(Snake);
            }
            else
            {
                SnakeCrashed?.Invoke(newHeadPosition);
                _moveDirection = Point.Empty;
            }
        }
        
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
                    PlayerHasKey = true;
                    PlayerGotKey?.Invoke();
                    break;
            }
            return true;
        }

        private bool TryOpenChest(Point chestPosition, bool byExplosion = false)
        {
            if (PlayerHasKey)
            {
                Score += 5;
                PlayerHasKey = false;
                ChestOpened?.Invoke(chestPosition);
                PlayerUsedKey?.Invoke();
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
            Fruits.Remove(fruitPosition);
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
            if (_leftStepsToTailExplosion > 0)
            {
                MakeGameOver(GameOverReason.AteTail);
                return;
            }
            _leftStepsToTailExplosion = StepsToTailExplosion;
            SnakeTail = eatenParts;
            if (!byExplosion)
                SnakeAteSelfPart?.Invoke(eatenParts);
        }

        private bool SpawnItem(FieldObjects itemType , int probability, int maxItemCount = 0,
            HashSet<Point> items = null, bool itemState = true)
        {
            var randomGenerator = new Random(new Random().Next());
            var spawnItem = randomGenerator.Next(MaxProbabilityValue);

            if (spawnItem < MaxProbabilityValue - probability || itemState && 
                (items == null || items.Count >= maxItemCount && items.Count != 0))
                return true;
            var fieldArea = _fieldSize.Width * _fieldSize.Height;
            for (var count = 0; count < fieldArea; count++)
            {
                var xPos = randomGenerator.Next(0, _fieldSize.Width);
                var yPos = randomGenerator.Next(0, _fieldSize.Height);
                if (_field[xPos, yPos] != FieldObjects.Empty) continue;

                _field[xPos, yPos] = itemType;
                items?.Add(new Point(xPos, yPos));
                return true;
            }
            return false;
        }
    }
}