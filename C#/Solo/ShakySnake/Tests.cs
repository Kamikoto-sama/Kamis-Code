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
            var snake = new Snake(Point.Empty);
            for (var i = 0; i < 5; i++)
            {
                snake.AddPart();
                snake.MoveAfterHead(new Point(i + 1, 0));
            }
            var tail = snake.CutTail(new Point(4, 0));
            var expected = Enumerable.Range(-3, 4)
                .Select(x => new Point(-x, 0))
                .ToList();
            
            Assert.AreEqual(1, snake.Length);
            Assert.AreEqual(expected, tail);
        }
        
        [TestCase(Direction.Right, TestName = "Go right")]
        [TestCase(Direction.Left, TestName = "Go left")]
        [TestCase(Direction.Down, TestName = "Go down")]
        [TestCase(Direction.Up, TestName = "Go up")]
        public void CorrectWhenHeadOutOfBounds(Direction direction)
        {
            var gameModel = new GameModel(new Size(2, 2), Point.Empty, Direction.Right);
            gameModel.MoveDirection = direction;
            for (var i = 0; i < 2; i++)
                gameModel.Update();
            var actual = gameModel.Snake.Head.Value;
            
            Assert.AreEqual(Point.Empty, actual);
        }
        
        [Test]
        public void WhenEatFruit()
        {
            var gameModel = new GameModel(new Size(2, 2), Point.Empty, Direction.Right);
            gameModel.Update();
            gameModel.MoveDirection = Direction.Down;
            gameModel.Update();
            gameModel.MoveDirection = Direction.Left;
            gameModel.Update();
            gameModel.MoveDirection = Direction.Up;
            
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