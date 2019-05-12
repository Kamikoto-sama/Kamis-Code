using System.Drawing;
using NUnit.Framework;

namespace ShakySnake
{
    [TestFixture]
    public class Tests
    {
        [Test]
        public void SnakeAddPart()
        {
            var snake = new Snake(new Point(1, 1));
            for (var i = 0; i < 5; i++) snake.AddPart();
            Assert.AreEqual(6, snake.Lenght);
        }
        
        [Test]
        public void CutTail()
        {
            var snake = new Snake(new Point(1, 1));
            for (var i = 0; i < 5; i++) snake.AddPart();
            snake.CutTail(Point.Empty);
            Assert.AreEqual(1, snake.Lenght);
        }
    }
}