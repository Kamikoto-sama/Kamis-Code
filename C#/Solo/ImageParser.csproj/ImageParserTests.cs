using System.IO;
using System.Reflection;
using System.Text.RegularExpressions;
using System.Xml;
using NUnit.Framework;

namespace ImageParser
{
    [TestFixture]
    public class ImageParserTests
    {
        private const string _filesPath = @"D:\My_Programms\C#\Solo\ImageParser.csproj\bin\Debug\";
        private ImageParser parser;

        [SetUp]
        public void SetUp()
        {
            parser = new ImageParser();
        }

        [TestCase("Png", 229983)]
        [TestCase("Gif", 65281)]
        [TestCase("Bmp", 747658)]
        public void SimpleConvert(string format, int fileSize)
        {
            var path = $"{_filesPath}image.{format}";
            var image = new FileStream(path, FileMode.Open, FileAccess.Read);
            var result = parser.GetImageInfo(image);
            var expected = $"{{\"Height\":292,\"Width\":640,\"Format\":\"{format}\",\"Size\":{fileSize}}}";
            var replaced = Regex.Replace(result, @"\s+", "");
            Assert.AreEqual(expected, replaced);
        }
        
        [TestCase(1, 640, 292)]
        [TestCase(2, 1920, 1080)]
        [TestCase(3, 1280, 720)]
        [TestCase(4, 2048, 1280)]
        [TestCase(5, 540, 720)]
        [TestCase(6, 1714, 2749)]
        [TestCase(7, 508, 723)]
        public void BMPSize(int number, int width, int height) 
            => ImageSize(ImageFormats.Bmp, number, width, height);

        [TestCase(1, 640, 292)]
        [TestCase(2, 320, 320)]
        [TestCase(3, 560, 315)]
        [TestCase(4, 499, 281)]
        [TestCase(5, 390, 600)]
        public void GIFSize(int number, int width, int height) 
            => ImageSize(ImageFormats.Gif, number, width, height);

        private void ImageSize(ImageFormats imgType,int number, int width, int height)
        {
            var path = $"{_filesPath}{imgType}/image{number}.{imgType}";
            var image = new FileStream(path, FileMode.Open, FileAccess.Read);
            image.Position += 1;
            var getImageSize = typeof(ImageParser)
                .GetMethod("GetImageSize", BindingFlags.NonPublic | BindingFlags.Static);
            var size = (ImageSize) getImageSize.Invoke(null, new object[] {image, imgType});
            Assert.AreEqual(width, size.Width);
            Assert.AreEqual(height, size.Height);
        }
    }
}