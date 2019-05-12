using System.Drawing;
using System.Reflection;
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
        
        [TestCase(1, 1, 1, 0, TestName = "Go right")]
        [TestCase(1, 1, 0, 1, TestName = "Go down")]
        [TestCase(0, 0,-1, 0, TestName = "Go left")]
        [TestCase(0, 0, 0, -1, TestName = "Go up")]
        public void MakeInBoundsWhenHeadOutOfFieldRange(int initX, int initY,
            int xDirection, int yDirection)
        {
            var gameModel = new GameModel(1, Point.Empty);
            gameModel.MoveDirection = new Point(initX, initY);
            gameModel.MoveSnake();
        }
    }
}