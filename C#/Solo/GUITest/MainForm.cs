using System;
using System.Drawing;
using System.Linq;
using System.Windows.Forms;

namespace GUITest
{
    public class MainForm: Form
    {
        private Label _label;
        private TextBox _textBox;
        private Control.ControlCollection self;

        public MainForm()
        {
            _label = new Label();
            _textBox = new TextBox
            {
                Size = new Size(Width, 50),
                Location = new Point(0, _label.Bottom + 2)
            };

            self = Controls;
            self.Add(_label);
            self.Add(_textBox);

            this.StartPosition = FormStartPosition.CenterScreen;
            KeyPress += Escape;
        }

        private void Escape(object sender, KeyPressEventArgs args)
        {
            if (args.KeyChar == (char)Keys.Escape)
                this.Close();
        }
    }
}