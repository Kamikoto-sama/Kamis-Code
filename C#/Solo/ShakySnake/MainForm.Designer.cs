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
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this._timer = new System.Windows.Forms.Timer(this.components);
            this._mainField = new System.Windows.Forms.Panel();
            this._gameScore = new System.Windows.Forms.Label();
            this.SuspendLayout();
            this._timer.Tick += new System.EventHandler(this.UpdateView);
            this._mainField.Location = new System.Drawing.Point(12, 35);
            this._mainField.Name = "_mainField";
            this._mainField.Size = new System.Drawing.Size(543, 514);
            this._mainField.TabIndex = 0;
            this._gameScore.AutoSize = true;
            this._gameScore.Location = new System.Drawing.Point(12, 9);
            this._gameScore.Name = "_gameScore";
            this._gameScore.Size = new System.Drawing.Size(78, 23);
            this._gameScore.TabIndex = 1;
            this._gameScore.Text = "Score: 0";
            this.AutoScaleDimensions = new System.Drawing.SizeF(10F, 23F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(565, 561);
            this.Controls.Add(this._gameScore);
            this.Controls.Add(this._mainField);
            this.DoubleBuffered = true;
            this.Font = new System.Drawing.Font("Comic Sans MS", 12F, System.Drawing.FontStyle.Bold,
                System.Drawing.GraphicsUnit.Point, ((byte) (204)));
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

        private System.Windows.Forms.Panel _mainField;
        private System.Windows.Forms.Label _gameScore;
        private System.Windows.Forms.Timer _timer;
    }
}

