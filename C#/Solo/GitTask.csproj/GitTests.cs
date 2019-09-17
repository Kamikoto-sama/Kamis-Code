using NUnit.Framework;

namespace GitTask
{
    [TestFixture]
    public class GitTests
    {
        private const int DefaultFilesCount = 5;
        private Git _git;

        [SetUp]
        public void SetUp()
        {
            _git = new Git(DefaultFilesCount);
        }

        [Test]
        public void SimpleTest()
        {
            _git.Update(0, 5);
            Assert.AreEqual(0, _git.Commit());
            _git.Update(0, 6);
            Assert.AreEqual(5, _git.Checkout(0, 0));
        }
        
        [Test]
        public void NoUpdate_Commit_Checkout()
        {
            var git = new Git(3);
            git.Commit();
            Assert.AreEqual(0, git.Checkout(0, 0));
            Assert.AreEqual(0, git.Checkout(0, 1));
            Assert.AreEqual(0, git.Checkout(0, 2));
        }
        
        [Test]
        public void Update_Commit_Each_Once()
        {
            var git = new Git(5);
            for (var i = 0; i < 5; i++)
            {
                git.Update(i, i + 1);
                git.Commit();
            }

            for (var i = 0; i < 5; i++)
            {
                Assert.AreEqual(i + 1, git.Checkout(i, i));
            }
        }
   }
}