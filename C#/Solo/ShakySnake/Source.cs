using System;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;

namespace ShakySnake
{
    public static class Source
    {
        public const string Path = @"../../Resources/";
        public const string ImageFormat = ".png";

        public static Image GetImage(string imageName)
        {
            try
            {
                return Image.FromFile(Path + imageName + ImageFormat);
            }
            catch (System.IO.FileNotFoundException)
            {
                return Image.FromFile(Path + "Default" + ImageFormat);
            }
        }
    }
}