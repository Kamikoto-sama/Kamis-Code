using System.Drawing;
using System.Linq;
using System.Reflection;
using System.Text;
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
            
            Assert.AreEqual(6, snake.Length);
        }
        
        [Test]
        public void SnakeCutsTail()
        {
            var snake = new Snake(new Point(1, 1));
            for (var i = 0; i < 5; i++) snake.AddPart();
            var tail = snake.CutTail(Point.Empty);
            var expected = new Point[5];
            
            Assert.AreEqual(1, snake.Length);
            Assert.AreEqual(expected, tail);
        }
        
        [TestCase(1, 0, TestName = "Go right")]
        [TestCase(-1, 0, TestName = "Go left")]
        [TestCase(0, 1, TestName = "Go down")]
        [TestCase(0, -1, TestName = "Go up")]
        public void CorrectWhenHeadOutOfBounds(int directionX, int directionY)
        {
            var gameModel = new GameModel(new Size(2, 2), Point.Empty);
            gameModel.MoveDirection = new Point(directionX, directionY);
            for (var i = 0; i < 2; i++)
                gameModel.Update();
            var actual = gameModel.Snake.Head.Value;
            
            Assert.AreEqual(Point.Empty, actual);
        }
        
        [Test]
        public void WhenEatFruit()
        {
            var gameModel = new GameModel(new Size(2, 2), Point.Empty);
            gameModel.MoveDirection = new Point(1 , 0);
            gameModel.Update();
            gameModel.MoveDirection = new Point(0 , 1);
            gameModel.Update();
            gameModel.MoveDirection = new Point(-1 , 0);
            gameModel.Update();
            gameModel.MoveDirection = new Point(0 , -1);
            
            Assert.IsTrue(gameModel.Score > 0, "Score > 0");
            Assert.IsTrue(gameModel.Snake.Length > 1, "Snake length > 1");
        }
        
        [Test]
        public void SnakeMovesAfterHead()
        {
            var snake = new Snake(Point.Empty);
            snake.AddPart();
            snake.MoveAfterHead(new Point(1, 0));
            snake.AddPart();
            snake.MoveAfterHead(new Point(2, 0));
            snake.AddPart();
            snake.MoveAfterHead(new Point(3, 0));

            var expectedSnakeParts = new[]
            {
                new Point(3, 0), new Point(2, 0), new Point(1, 0),
                new Point(0, 0)
            };
            Assert.AreEqual(expectedSnakeParts, snake.Parts.ToArray());
        }
    }
}