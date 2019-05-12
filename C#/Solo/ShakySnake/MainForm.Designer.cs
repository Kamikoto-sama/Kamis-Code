namespace ShakySnake
{
    partial class MainForm
    {
        /// <summary>
        /// Обязательная переменная конструктора.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Освободить все используемые ресурсы.
        /// </summary>
        /// <param name="disposing">истинно, если управляемый ресурс должен быть удален; иначе ложно.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Код, автоматически созданный конструктором форм Windows

        /// <summary>
        /// Требуемый метод для поддержки конструктора — не изменяйте 
        /// содержимое этого метода с помощью редактора кода.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this._timer = new System.Windows.Forms.Timer(this.components);
            this._field = new System.Windows.Forms.Panel();
            this._gameScore = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // _timer
            // 
            this._timer.Enabled = true;
            this._timer.Tick += new System.EventHandler(this.UpdateView);
            // 
            // _field
            // 
            this._field.Location = new System.Drawing.Point(12, 12);
            this._field.Name = "_field";
            this._field.Size = new System.Drawing.Size(500, 500);
            this._field.TabIndex = 0;
            // 
            // _gameScore
            // 
            this._gameScore.AutoSize = true;
            this._gameScore.Location = new System.Drawing.Point(518, 12);
            this._gameScore.Name = "_gameScore";
            this._gameScore.Size = new System.Drawing.Size(78, 23);
            this._gameScore.TabIndex = 1;
            this._gameScore.Text = "Score: 0";
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(10F, 23F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(676, 529);
            this.Controls.Add(this._gameScore);
            this.Controls.Add(this._field);
            this.DoubleBuffered = true;
            this.Font = new System.Drawing.Font("Comic Sans MS", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(204)));
            this.Margin = new System.Windows.Forms.Padding(5);
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "MainForm";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "MainForm";
            this.KeyDown += new System.Windows.Forms.KeyEventHandler(this.MainForm_KeyDown);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion
        private System.Windows.Forms.Panel _field;
        private System.Windows.Forms.Label _gameScore;
        private System.Windows.Forms.Timer _timer;
    }
}

