using System;
using System.ComponentModel;
using System.Drawing;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace GUITest
{
    public class MainForm: Form
    {
        private Label _label;
        private Control.ControlCollection self;
        private Button _button;
        private ProgressBar _progress;

        public MainForm()
        {
            self = Controls;

            _label = new Label{Size = new Size(Width - 20, 20)};
            _button = new Button
            {
                Location = new Point(0, _label.Bottom),
                Size = _label.Size
            };
            _progress = new ProgressBar
            {
                Location = new Point(0, _button.Bottom),
                Size = _label.Size
            };            
            
            self.Add(_label);
            self.Add(_progress);
            self.Add(_button);
            _button.Click += (sender, args) => Work();

            this.StartPosition = FormStartPosition.CenterScreen;
        }

        private void Work()
        {
            var task = new BackgroundWorker{WorkerReportsProgress = true};
            task.DoWork += DoWork;
            task.RunWorkerCompleted += (sender, args) => _label.Text = "DONE";
            task.ProgressChanged += (sender, args) => _progress.Value = args.ProgressPercentage;
            task.RunWorkerAsync();
        }

        private void DoWork(object sender, DoWorkEventArgs e)
        {
            var worker = sender as BackgroundWorker;
            for (var i = 0; i < 100; i++)
            {
                Thread.Sleep(50);
                worker.ReportProgress(i);
            }
        }
    }
}