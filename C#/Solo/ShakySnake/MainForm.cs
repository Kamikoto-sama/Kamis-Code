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
        
        public MainForm()
        {
            InitializeComponent();
            
            this.Controls.Add();
        }

        private void MainForm_KeyDown(object sender, KeyEventArgs e)
        {
            var key = e.KeyCode;
            if(Enum.TryParse(key.ToString(), out Direction direction)
            && Math.Abs(_moveDirection - direction) != 2)
                _moveDirection = direction;
            else if(key == Keys.Escape)
                this.Close();
        }

        private void ViewModel(object sender, EventArgs e)
        {
            _player.Move(_moveDirection, _step);
            
            Head.Location = _player.Head;
            var rotationValue = _headDirection - _moveDirection;
            if(Math.Abs(rotationValue) != 0) 
                RotateHead(rotationValue);
        }
    }
}
