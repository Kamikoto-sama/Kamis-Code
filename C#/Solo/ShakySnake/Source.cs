using System.Collections.Generic;

namespace ShakySnake
{
    public static class Source
    {
        public const string Path = @"../../Resources/";

        public static readonly Dictionary<string, string> SnakeHead =
            new Dictionary<string, string>
            {
                {"Up", Path + "SnakeHeadUp.png"},
                {"Down", Path + "SnakeHeadDown.png"},
                {"Left", Path + "SnakeHeadLeft.png"},
                {"Right", Path + "SnakeHeadRight.png"},
            };
        
        public static readonly Dictionary<string, string> SnakeParts =
            new Dictionary<string, string>
            {
                {"Up", Path + "SnakePart.png"},
                {"Down", Path + "SnakePart.png"},
                {"Left", Path + "SnakePart.png"},
                {"Right", Path + "SnakePart.png"},
            };
    }
}