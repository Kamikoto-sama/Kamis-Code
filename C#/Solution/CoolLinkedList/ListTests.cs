using System.Runtime.Remoting.Lifetime;
using NUnit.Framework;

namespace LinkedList
{
    [TestFixture]
    public class ListTests
    {
        [Test]
        public void ItWorks()
        {
            var list = new CoolLinkedList<int>();
            list.AddLast(1);
            list.AddLast(2);
            list.AddLast(3);
            Assert.AreEqual(3, list.Count);
            Assert.AreEqual(1, list[0]);
            Assert.AreEqual(2, list[1]);
            Assert.AreEqual(3, list[2]);
        }
    }
}