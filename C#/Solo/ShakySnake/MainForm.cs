using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using UsefulExtensions;

namespace ShakySnake
{
    public partial class MainForm : Form
    {
        private const int _updateInterval = 100;
        private const int _fieldSize = 10;
        private readonly GameModel _gameModel;
        
        public MainForm()
        {
            InitializeComponent();
            _gameModel = new GameModel(_fieldSize, Point.Empty);
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

        void UpdateGameModel()
        {
            _gameModel.MoveSnake();
        }
    }
}
