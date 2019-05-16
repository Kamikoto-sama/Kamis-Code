using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Windows.Forms;

namespace ShakySnake
{
    public partial class MainForm : Form
    {
        private const int _updateInterval = 100;
        private const int _cellSize = 25;
        private Size _fieldSize => 
            new Size(_mainField.Width / _cellSize, _mainField.Height / _cellSize);
        
        private readonly Point _initialPosition = Point.Empty;
        private readonly GameModel _gameModel;
        private readonly List<PictureBox> _snakeView;
        private readonly PictureBox[,] _fieldView;
        private List<PictureBox> _cutTail;
        private List<Point> _blownObjects;
        private int _explosionTimer = -1;
        
        public MainForm()
        {
            InitializeComponent();
            AlignFieldToCellSize();
            _gameModel = new GameModel(_fieldSize, _initialPosition, Direction.Right);
            _fieldView = new PictureBox[_fieldSize.Width, _fieldSize.Height];
            HundleGameModelEvents();
            _snakeView = new List<PictureBox>();
            CreateHead();
            _viewTimer.Interval = _updateInterval;
            _viewTimer.Start();
        }

        private void HundleGameModelEvents()
        {
            _gameModel.SnakeMoved += OnSnakeMoved;
            _gameModel.FruitEaten += OnFruitEaten;
            _gameModel.SnakeAteSelfPart += OnSnakeAteItSelf;
            _gameModel.GameOver += OnGameOver;
            _gameModel.ItemAppeared += DrawItem;
            _gameModel.SnakeCrashed += OnSnakeCrashed;
            _gameModel.PlayerGotKey += OnGetKey;
            _gameModel.PlayerUsedKey += OnPlayerUsedKey;
            _gameModel.ObjectsBlown += OnObjectsBlown;
        }

        private void AlignFieldToCellSize()
        {
            var widthAlign = _cellSize * (_mainField.Width / _cellSize);
            var heightAlign = _cellSize * (_mainField.Height / _cellSize);
            var widthShift = _mainField.Width - widthAlign;
            var heightShift = _mainField.Height - heightAlign;
            _mainField.Size = new Size(widthAlign, heightAlign);
            this.Size -= new Size(widthShift, heightShift);
        }

        private void OnGameOver(GameOverReason gameOverReasonType)
        {
            _viewTimer.Stop();
            var text = gameOverReasonType == GameOverReason.HeadBlown ? 
                "Oh shit your head has blown! XD" : 
                "Your can't left move than one tail! :(";
            MessageBox.Show(text, "Game is over!");
            this.Close();
        }

        private void OnSnakeAteItSelf(List<Point> eatenParts)
        {
            var partsCount = eatenParts.Count + 1;
            _cutTail = _snakeView.GetRange(_snakeView.Count - partsCount, partsCount);
            _snakeView.RemoveRange(_snakeView.Count - partsCount, partsCount);
        }
        
        private void OnObjectsBlown(List<Point> objects, FieldObjects blownReason)
        {
            var image = Source.GetImage("Explosion");
            if (blownReason == FieldObjects.LostSnakeTail)
                foreach (var part in _cutTail)
                    part.Image = image;
            foreach (var obj in objects)
                _fieldView[obj.X, obj.Y].Image = image;
            _explosionTimer = 3;
            _blownObjects = objects;
        }
        
        private void ClearExplosion()
        {
            if (_cutTail != null)
                foreach (var part in _cutTail)
                    _mainField.Controls.Remove(part);
            _cutTail = null;
            if (_blownObjects != null)
                foreach (var blownObject in _blownObjects)
                    RemoveObject(blownObject);
            _blownObjects = null;
        }

        private void OnGetKey(Point position)
        {
            RemoveObject(position);
            _keyBox.Location = new Point(_gameScore.Right + 10, 5);
            _keyBox.Image = Source.GetImage("KeyIcon");
            _keyBox.Visible = true;
        }

        private void RemoveObject(Point objPosition)
        {
            var obj = _fieldView[objPosition.X, objPosition.Y];
            _mainField.Controls.Remove(obj);
            _fieldView[objPosition.X, objPosition.Y] = null;
        }
        
        private void OnPlayerUsedKey(Point position)
        {
            RemoveObject(position);
            _keyBox.Visible = false;
        }
        
        private void OnSnakeCrashed(Point position)
        {
            MessageBox.Show("You've crashed, choose another direction");
        }
        
        private void DrawItem(Point position, FieldObjects objType)
        {
            var location = new Point(position.X * _cellSize, position.Y * _cellSize);
            var newItem = new PictureBox();
            newItem.Image = Source.GetImage(objType.ToString());
            newItem.Size = new Size(_cellSize, _cellSize);
            newItem.Location = location;
            if (_fieldView[position.X, position.Y] == null)
            {
                _fieldView[position.X, position.Y] = newItem;
                _mainField.Controls.Add(newItem);
            }
            else
            {
                RemoveObject(position);
                DrawItem(position, objType);
            }
        }

        private void CreateHead()
        {
            var head = new PictureBox
            {
                Size = new Size(_cellSize, _cellSize),
                Location = _initialPosition
            };
            _snakeView.Add(head);
            _mainField.Controls.Add(head);
        }

        private void OnSnakeMoved(Snake snake)
        {
            var partIndex = 0;
            _snakeView[0].Image = Source.GetImage(FieldObjects.SnakeHead.ToString() +
                                                    _gameModel.MoveDirection);
            foreach (var snakePart in snake.Parts)
            {
                var position = new Point(snakePart.X * _cellSize,
                                         snakePart.Y * _cellSize);
                _snakeView[partIndex].Location = position;
                partIndex++;
            }
        }
        
        private void OnFruitEaten(Point fruitPosition)
        {
            RemoveObject(fruitPosition);
            var newPart = new PictureBox
            {
                Image = Source.GetImage($"{FieldObjects.SnakePart}"),
                Size = new Size(_cellSize, _cellSize),
                Location = _gameModel.Snake.Tail.Value
            };
            _snakeView.Add(newPart);
            _mainField.Controls.Add(newPart);
        }
        
        private void MainForm_KeyDown(object sender, KeyEventArgs e)
        {
            var key = e.KeyCode;
            switch (key)
            {
                case Keys.Up:
                    _gameModel.MoveDirection = Direction.Up;
                    break;
                case Keys.Right:
                    _gameModel.MoveDirection = Direction.Right;
                    break;
                case Keys.Down:
                    _gameModel.MoveDirection = Direction.Down;
                    break;
                case Keys.Left:
                    _gameModel.MoveDirection = Direction.Left;
                    break;
                case Keys.Escape:
                    this.Close();
                    break;
            }
        }
        
        private void UpdateView(object sender, EventArgs e)
        {
            _gameModel.Update();
            _gameScore.Text = $"Score: {_gameModel.Score}";
            if (_explosionTimer == 0)
                ClearExplosion();
            else
                _explosionTimer--;
        }
    }
}
