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
        private Point _playerInitialPosition = Point.Empty;

        private GameModel _gameModel;
        private List<PictureBox> _snakeView;
        private PictureBox[,] _fieldView;
        
        public MainForm()
        {
            InitializeComponent();
            AlignFieldToCellSize();
            _timer.Interval = _updateInterval;
            _gameModel = new GameModel(_fieldSize, _playerInitialPosition, new Point(1, 0));
            HundleGameModelEvents();
            _snakeView = new List<PictureBox>();
            CreateHead();
            _timer.Start();
        }

        private void HundleGameModelEvents()
        {
            _gameModel.SnakeMoved += OnSnakeMoved;
            _gameModel.FruitEaten += OnFruitEaten;
            _gameModel.SnakeAteSelfPart += OnSnakeAteItSelf;
            _gameModel.GameOver += OnGameOver;
        }

        void AlignFieldToCellSize()
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
            _timer.Stop();
            var text = $"Your score is: {_gameModel.Score}";
            MessageBox.Show(text, "Game is over!");
            this.Close();
        }

        private void OnSnakeAteItSelf(List<Point> eatenParts)
        {
            var partsCount = eatenParts.Count;
            foreach (var part in _snakeView.Skip(_snakeView.Count - partsCount))
                part.Dispose();
            _snakeView.RemoveRange(_snakeView.Count - partsCount, partsCount);
        }

        private void DrawFruit()
        {
            var fruitPosition = _gameModel.Fruits;
            fruitPosition = new Point(fruitPosition.X * _cellSize, 
                                          fruitPosition.Y * _cellSize);
            if (_fruit == null)
            {
                var fruit = new PictureBox();
                fruit.BackColor = Color.Gold;
                fruit.Size = new Size(_cellSize, _cellSize);
                _mainField.Controls.Add(fruit);
                _fruit = fruit;
            }
            _fruit.Location = fruitPosition;
        }

        void CreateHead()
        {
            var head = new PictureBox
            {
                Size = new Size(_cellSize, _cellSize),
                Location = _playerInitialPosition
            };
            _snakeView.Add(head);
            _mainField.Controls.Add(head);
        }

        void OnSnakeMoved(Snake snake)
        {
            var partIndex = 0;
            foreach (var snakePart in snake.Parts)
            {
                var position = new Point(snakePart.X * _cellSize,
                                         snakePart.Y * _cellSize);
                _snakeView[partIndex].Location = position;
                RotateSnakePart(_gameModel.MoveDirection, _snakeView[partIndex],
                                partIndex == 0);
                partIndex++;
            }
        }
        
        void RotateSnakePart(Point newDirection, PictureBox part, bool isHead)
        {
            var direction = newDirection.X == 1 ? "Right" :
                newDirection.X == -1 ? "Left" :
                newDirection.Y == 1 ? "Down" : "Up";

            var image = isHead ? Source.SnakeHead[direction] :
                                Source.SnakeParts[direction];
            part.Image = new Bitmap(image);
        }
        
        private void OnFruitEaten(Point fruitPosition)
        {
            var newPart = new PictureBox
            {
                BackColor = Color.FromArgb(144, 197, 15),
                Size = new Size(_cellSize, _cellSize),
                Location = _gameModel.Snake.Tail.Value
            };
            _snakeView.Add(newPart);
            _mainField.Controls.Add(newPart);
        }
        
        private void MainForm_KeyDown(object sender, KeyEventArgs e)
        {
            var key = e.KeyCode;
            int xShift = 0, yShift = 0;
            switch (key)
            {
                case Keys.Up:
                    yShift--;
                    break;
                case Keys.Right:
                    xShift++;
                    break;
                case Keys.Down:
                    yShift++;
                    break;
                case Keys.Left:
                    xShift--;
                    break;
                case Keys.Escape:
                    this.Close();
                    break;
            }
            _gameModel.MoveDirection = new Point(xShift, yShift);   
        }
        
        private void UpdateView(object sender, EventArgs e)
        {
            _gameModel.Update();
            DrawFruit();
            _gameScore.Text = $"Score: {_gameModel.Score}";
        }
    }
}
