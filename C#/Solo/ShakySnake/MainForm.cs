using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Net.Mime;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using UsefulExtensions;

namespace ShakySnake
{
    public partial class MainForm : Form
    {
        private const int _updateInterval = 100;
        private const int _fieldSize = 20;
        private const int _cellSize = 25;
        private readonly Point _playerInitialPosition = Point.Empty;
        private readonly GameModel _gameModel;
        private readonly List<PictureBox> _snakeView;
        private PictureBox _head => _snakeView.FirstOrDefault();
        
        public MainForm()
        {
            InitializeComponent();
            _timer.Interval = _updateInterval;
            _gameModel = new GameModel(_fieldSize, _playerInitialPosition);
            _gameModel.SnakeMoved += OnSnakeMoved;
            _gameModel.FruitEaten += OnFruitEaten;
            _gameModel.FruitSpawned += OnFruitSpawned;
            _snakeView = new List<PictureBox>();
            CreateHead();
        }

        private void OnFruitSpawned(Point position)
        {
            var pos = new Point(position.X * _cellSize, position.Y * _cellSize);
            var fruit = new PictureBox();
            fruit.Location = pos;
            fruit.BackColor = Color.Gold;
            fruit.Size = new Size(_cellSize, _cellSize);
        }

        void CreateHead()
        {
//            var headImage = new Bitmap("../../Resources/SnakeHead.png");
            var head = new PictureBox
            {
                BackColor = Color.Red,
                Size = new Size(_cellSize, _cellSize),
                Location = _playerInitialPosition
            };
            _snakeView.Add(head);
            _field.Controls.Add(head);
        }

        void OnSnakeMoved(Snake snake)
        {
            var partIndex = 0;
            foreach (var snakePart in snake.Parts)
            {
                var position = new Point(snakePart.X * _cellSize,
                                         snakePart.Y * _cellSize);
                _snakeView[partIndex].Location = position;
                partIndex++;
            }
        }
        
        private void OnFruitEaten(Snake snake)
        {
            _gameScore.Text = $"Score: {_gameModel.Score}";
            
            var newPart = new PictureBox
            {
                BackColor = Color.PaleGreen,
                Size = new Size(_cellSize, _cellSize),
                Location = snake.Tail.Value
            };
            _snakeView.Add(newPart);
            _field.Controls.Add(newPart);
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
            }
            _gameModel.MoveDirection = new Point(xShift, yShift);   
        }
        
        private void UpdateView(object sender, EventArgs e)
        {
            _gameModel.MoveSnake();
        }
    }
}
