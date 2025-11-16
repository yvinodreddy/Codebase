// RMMS.Common/Extensions/StringExtensions.cs
using System;
using System.Globalization;
using System.Text.RegularExpressions;

namespace RMMS.Common.Extensions
{
    public static class StringExtensions
    {
        public static string ToTitleCase(this string str)
        {
            if (string.IsNullOrWhiteSpace(str))
                return str;

            TextInfo textInfo = CultureInfo.CurrentCulture.TextInfo;
            return textInfo.ToTitleCase(str.ToLower());
        }

        public static string Truncate(this string str, int maxLength)
        {
            if (string.IsNullOrEmpty(str))
                return str;

            return str.Length <= maxLength ? str : str.Substring(0, maxLength) + "...";
        }

        public static string RemoveSpecialCharacters(this string str)
        {
            if (string.IsNullOrEmpty(str))
                return str;

            return Regex.Replace(str, @"[^a-zA-Z0-9\s]", "");
        }
    }
}
