using System;
using System.Drawing;
using System.Linq;
using System.Windows.Forms;

namespace GUITest
{
    public class MainForm: Form
    {
        public Button split;
        public TextBox firstWord;
        public TextBox secondWord;
        public Label leftPart;
        public Label rightPart;
        
        public MainForm()
        {
            this.StartPosition = FormStartPosition.CenterScreen;

            this.firstWord = new TextBox();
            this.secondWord = new TextBox
            {
                Location = new Point(firstWord.Right + 5, 0)
            };
            this.split = new Button
            {
                Location = new Point(0, firstWord.Bottom + 5),
                Text = "Press",
                Size = firstWord.Size
            };
            this.leftPart = new Label
            {
                Location = new Point(0, split.Bottom + 5),
                Text = "Left",
            };
            this.rightPart = new Label
            {
                Location = new Point(leftPart.Right + 5, leftPart.Top),
                Text = "Right",
            };
            var self = Controls;
            self.Add(rightPart);
            self.Add(leftPart);
            self.Add(split);
            self.Add(firstWord);
            self.Add(secondWord);
            split.Click += MakeSplit;
            firstWord.KeyPress += EnterPressed;
            secondWord.KeyPress += EnterPressed;
        }

        void EnterPressed(object obj, KeyPressEventArgs args)
        {
            var enter = (char) Keys.Enter;
            if(args.KeyChar == enter)
                MakeSplit(obj, args);
        }
        
        void MakeSplit(object obj, EventArgs args)
        {
            var text1 = firstWord.Text;
            var text2 = secondWord.Text;
            if(text1.Length < 2 || text2.Length < 2)
                return;
            var left1 = text1.Remove(text1.Length / 2);
            var left2 = text2.Remove(text2.Length / 2);
            var right1 = text1.Remove(0, text1.Length / 2);
            var right2 = text2.Remove(0, text2.Length / 2);
            leftPart.Text = left1 + right2;
            rightPart.Text = left2 + right1;
        }
    }
}