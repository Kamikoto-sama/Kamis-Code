using System;
using System.IO;
using System.Linq;
using Newtonsoft.Json.Linq;
using System.Globalization;
using System.Collections.Generic;

namespace ImageParser
{
    public enum ImageFormats
    {
        Png, Bmp, Gif
    }
    
    public class ImageParser : IImageParser
    {
        private const int GifSignatureOffset = 5;
        private const int BmpSignatureAndMiscDataOffset = 2 + 13;
        private const int PngSignatureAndChunkHeadOffset = 7 + 8;

        public string GetImageInfo(Stream stream)
        {
            var format = GetImageFormat(stream);
            var imageSize = GetImageSize(stream, format);
            return ConvertToJson(imageSize, format);
        }

        private ImageFormats GetImageFormat(Stream stream)
        {
            var firstChar = stream.ReadByte();
            switch (firstChar)
            {
                case 'G':
                    return ImageFormats.Gif;
                case 'B':
                    return ImageFormats.Bmp;
                case 0x89:
                    return ImageFormats.Png;
                default:
                    throw new Exception("Unknown image format");
            }
        }

        private static ImageSize GetImageSize(Stream stream, ImageFormats format)
        {
            switch (format)
            {
                case ImageFormats.Png:
                    return ReadImagedSize(stream, PngSignatureAndChunkHeadOffset, 4, false);
                case ImageFormats.Gif:
                    return ReadImagedSize(stream, GifSignatureOffset, 2, true);
                case ImageFormats.Bmp:
                    return ReadImagedSize(stream, BmpSignatureAndMiscDataOffset, 4, true);
                default:
                    throw new Exception("Unknown image format");
            }
        }

        private static ImageSize ReadImagedSize(Stream stream, int offset, int dataSize, bool reverseBytePairs)
        {
            stream.Position += offset; // Move to image size data bytes
            var sizeBytes = new byte[dataSize];
            stream.Read(sizeBytes, 0, dataSize);
            var width = BytesToInt(sizeBytes, reverseBytePairs);
            stream.Read(sizeBytes, 0, dataSize);
            var height = BytesToInt(sizeBytes, reverseBytePairs);
            return new ImageSize(width, height, stream.Length);
        }

        private static int BytesToInt(IEnumerable<byte> numberParts, bool reverseBytePairs)
        {
            if (reverseBytePairs)
                numberParts = new[] {numberParts.Take(2), numberParts.Skip(2)}
                                .SelectMany(pair => pair.Reverse());
            var hex = string.Join("", numberParts.Select(b => b.ToString("X2")));
            return int.Parse(hex, NumberStyles.HexNumber);
        }
        
        private static string ConvertToJson(ImageSize imageSize, ImageFormats imageFormat)
        {
            var imageData = new JObject
            {
                {"Height", imageSize.Height},
                {"Width", imageSize.Width},
                {"Format", imageFormat.ToString()},
                {"Size", imageSize.FileSize}
            };
            return imageData.ToString();
        }
    }

    public struct ImageSize
    {
        public int Width { get; }
        public int Height { get; }
        public long FileSize { get; }

        public ImageSize(int width, int height, long fileSize)
        {
            Width = width;
            Height = height;
            FileSize = fileSize;
        }
    }
}