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
            this.MainLayout = new System.Windows.Forms.TableLayoutPanel();
            this.PanelTop = new System.Windows.Forms.Panel();
            this.MainField = new System.Windows.Forms.Panel();
            this.Head = new System.Windows.Forms.PictureBox();
            this.ViewTimer = new System.Windows.Forms.Timer(this.components);
            this.MainLayout.SuspendLayout();
            this.MainField.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.Head)).BeginInit();
            this.SuspendLayout();
            // 
            // MainLayout
            // 
            this.MainLayout.AutoSize = true;
            this.MainLayout.ColumnCount = 1;
            this.MainLayout.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.MainLayout.Controls.Add(this.PanelTop, 0, 0);
            this.MainLayout.Controls.Add(this.MainField, 0, 1);
            this.MainLayout.Dock = System.Windows.Forms.DockStyle.Fill;
            this.MainLayout.GrowStyle = System.Windows.Forms.TableLayoutPanelGrowStyle.FixedSize;
            this.MainLayout.Location = new System.Drawing.Point(0, 0);
            this.MainLayout.Margin = new System.Windows.Forms.Padding(0);
            this.MainLayout.Name = "MainLayout";
            this.MainLayout.RowCount = 2;
            this.MainLayout.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 50F));
            this.MainLayout.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.MainLayout.Size = new System.Drawing.Size(584, 611);
            this.MainLayout.TabIndex = 0;
            // 
            // PanelTop
            // 
            this.PanelTop.BackColor = System.Drawing.SystemColors.ControlDark;
            this.PanelTop.Dock = System.Windows.Forms.DockStyle.Fill;
            this.PanelTop.Location = new System.Drawing.Point(0, 0);
            this.PanelTop.Margin = new System.Windows.Forms.Padding(0);
            this.PanelTop.Name = "PanelTop";
            this.PanelTop.Size = new System.Drawing.Size(584, 50);
            this.PanelTop.TabIndex = 0;
            // 
            // MainField
            // 
            this.MainField.BackColor = System.Drawing.SystemColors.Highlight;
            this.MainField.Controls.Add(this.Head);
            this.MainField.Dock = System.Windows.Forms.DockStyle.Fill;
            this.MainField.Location = new System.Drawing.Point(0, 50);
            this.MainField.Margin = new System.Windows.Forms.Padding(0);
            this.MainField.Name = "MainField";
            this.MainField.Size = new System.Drawing.Size(584, 561);
            this.MainField.TabIndex = 1;
            // 
            // Head
            // 
            this.Head.BackColor = System.Drawing.SystemColors.Highlight;
            this.Head.Image = global::ShakySnake.Properties.Resources.SnakeHead;
            this.Head.Location = new System.Drawing.Point(0, 0);
            this.Head.Name = "Head";
            this.Head.Size = new System.Drawing.Size(50, 50);
            this.Head.TabIndex = 0;
            this.Head.TabStop = false;
            // 
            // ViewTimer
            // 
            this.ViewTimer.Enabled = true;
//            this.ViewTimer.Tick += new System.EventHandler(this.ViewModel);
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(10F, 23F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(584, 611);
            this.Controls.Add(this.MainLayout);
            this.Font = new System.Drawing.Font("Comic Sans MS", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(204)));
            this.Margin = new System.Windows.Forms.Padding(5);
            this.MinimumSize = new System.Drawing.Size(500, 500);
            this.Name = "MainForm";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "MainForm";
//            this.KeyDown += new System.Windows.Forms.KeyEventHandler(this.MainForm_KeyDown);
            this.MainLayout.ResumeLayout(false);
            this.MainField.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.Head)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TableLayoutPanel MainLayout;
        private System.Windows.Forms.Panel PanelTop;
        private System.Windows.Forms.PictureBox Head;
        private System.Windows.Forms.Timer ViewTimer;
        private System.Windows.Forms.Panel MainField;
    }
}

