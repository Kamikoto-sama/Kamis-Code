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
            this._mainField = new System.Windows.Forms.Panel();
            this._mainPanel = new System.Windows.Forms.Panel();
            this._keyBox = new System.Windows.Forms.PictureBox();
            this._gameScore = new System.Windows.Forms.Label();
            this._viewTimer = new System.Windows.Forms.Timer(this.components);
            this._mainPanel.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize) (this._keyBox)).BeginInit();
            this.SuspendLayout();
            // 
            // _mainField
            // 
            this._mainField.Location = new System.Drawing.Point(12, 60);
            this._mainField.Name = "_mainField";
            this._mainField.Size = new System.Drawing.Size(543, 489);
            this._mainField.TabIndex = 0;
            // 
            // _mainPanel
            // 
            this._mainPanel.Controls.Add(this._keyBox);
            this._mainPanel.Controls.Add(this._gameScore);
            this._mainPanel.Location = new System.Drawing.Point(12, 12);
            this._mainPanel.Name = "_mainPanel";
            this._mainPanel.Size = new System.Drawing.Size(543, 40);
            this._mainPanel.TabIndex = 1;
            // 
            // _keyBox
            // 
            this._keyBox.Location = new System.Drawing.Point(87, 5);
            this._keyBox.Name = "_keyBox";
            this._keyBox.Size = new System.Drawing.Size(32, 32);
            this._keyBox.TabIndex = 3;
            this._keyBox.TabStop = false;
            this._keyBox.Visible = false;
            // 
            // _gameScore
            // 
            this._gameScore.AutoSize = true;
            this._gameScore.Location = new System.Drawing.Point(6, 8);
            this._gameScore.Margin = new System.Windows.Forms.Padding(0);
            this._gameScore.Name = "_gameScore";
            this._gameScore.Size = new System.Drawing.Size(78, 23);
            this._gameScore.TabIndex = 2;
            this._gameScore.Text = "Score: 0";
            // 
            // _viewTimer
            // 
            this._viewTimer.Tick += new System.EventHandler(this.UpdateView);
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(10F, 23F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.SystemColors.Control;
            this.ClientSize = new System.Drawing.Size(565, 561);
            this.Controls.Add(this._mainPanel);
            this.Controls.Add(this._mainField);
            this.DoubleBuffered = true;
            this.Font = new System.Drawing.Font("Comic Sans MS", 12F, System.Drawing.FontStyle.Bold,
                System.Drawing.GraphicsUnit.Point, ((byte) (204)));
            this.Location = new System.Drawing.Point(15, 15);
            this.Margin = new System.Windows.Forms.Padding(5);
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "MainForm";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.KeyDown += new System.Windows.Forms.KeyEventHandler(this.MainForm_KeyDown);
            this._mainPanel.ResumeLayout(false);
            this._mainPanel.PerformLayout();
            ((System.ComponentModel.ISupportInitialize) (this._keyBox)).EndInit();
            this.ResumeLayout(false);
        }

        #endregion

        private System.Windows.Forms.Panel _mainField;
        private System.Windows.Forms.Label _gameScore;
        private System.Windows.Forms.PictureBox _keyBox;
        private System.Windows.Forms.Timer _viewTimer;
        private System.Windows.Forms.Panel _mainPanel;
    }
}

