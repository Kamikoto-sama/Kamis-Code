using System;
using System.Diagnostics;
using System.Drawing;

namespace SpaceName
{
	// ## Прочитайте! ##
	//
	// Ваша задача привести код в этом файле в порядок.
	// Для начала запустите эту программу. Для этого в VS в проект подключите сборку System.Drawing.

	// Переименуйте всё, что называется неправильно. Это можно делать комбинацией клавиш Ctrl+R, Ctrl+R (дважды нажать Ctrl+R).
	// Повторяющиеся части кода вынесите во вспомогательные методы. Это можно сделать выделив несколько строк кода и нажав Ctrl+R, Ctrl+M
	// Избавьтесь от всех зашитых в коде числовых констант — положите их в переменные с понятными именами.
	//
	// После наведения порядка проверьте, что ваш код стал лучше.
	// На сколько проще после ваших переделок стало изменить размер фигуры? Повернуть её на некоторый угол?
	// Научиться рисовать невозможный треугольник, вместо квадрата?

	class Painter
	{
		static Bitmap image = new Bitmap(800, 600);
		static float x, y;
		static Graphics graphics;

		public static void InitializeImage()
		{
			image = new Bitmap(800, 600);
			graphics = Graphics.FromImage(image);
		}

		public static void SetPos(float x0, float y0)
		{
			x = x0;
			y = y0;
		}

		public static void DrawPath(double length, double angle)
		{
			//Делает шаг длиной L в направлении angle и рисует пройденную траекторию
			var x1 = (float)(x + length * Math.Cos(angle));
			var y1 = (float)(y + length * Math.Sin(angle));
			graphics.DrawLine(Pens.Yellow, x, y, x1, y1);
			x = x1;
			y = y1;
		}

		public static void ShowResult()
		{
			image.Save("result.bmp");
			Process.Start("result.bmp");
		}
	}

	public class DrawSquare
	{
		public static void Main()
		{
			Painter.InitializeImage();

			//Рисуем четыре одинаковые части невозможного квадрата.
			Draw(10, 0, 0);
			Draw(120, 10, Math.PI / 2);
			Draw(110, 120, Math.PI);
			Draw(0, 110, -Math.PI);

			Painter.ShowResult();
		}

		public static void Draw(int x, int y, double angle)
		{
			Painter.SetPos(x, y);
			Painter.DrawPath(100, 0);
			Painter.DrawPath(10 * Math.Sqrt(2), Math.PI / 4 + angle);
			Painter.DrawPath(100, Math.PI + angle);
			Painter.DrawPath(100 - (double) 10, Math.PI / 2 + angle);
		}
	}
}