// RMMS.Common/Utilities/ValidationHelper.cs
using System;
using System.Text.RegularExpressions;

namespace RMMS.Common.Utilities
{
    public static class ValidationHelper
    {
        public static bool IsValidGSTIN(string gstin)
        {
            if (string.IsNullOrWhiteSpace(gstin))
                return false;

            // GSTIN pattern: 2 digits + 5 letters + 4 digits + 1 letter + 1 alphanumeric + Z + 1 alphanumeric
            string pattern = @"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[A-Z0-9]{1}[Z]{1}[A-Z0-9]{1}$";
            return Regex.IsMatch(gstin, pattern);
        }

        public static bool IsValidEmail(string email)
        {
            if (string.IsNullOrWhiteSpace(email))
                return false;

            string pattern = @"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$";
            return Regex.IsMatch(email, pattern);
        }

        public static bool IsValidMobile(string mobile)
        {
            if (string.IsNullOrWhiteSpace(mobile))
                return false;

            // Indian mobile number pattern
            string pattern = @"^[6-9]\d{9}$";
            return Regex.IsMatch(mobile, pattern);
        }

        public static bool IsValidPAN(string pan)
        {
            if (string.IsNullOrWhiteSpace(pan))
                return false;

            // PAN pattern: 5 letters + 4 digits + 1 letter
            string pattern = @"^[A-Z]{5}[0-9]{4}[A-Z]{1}$";
            return Regex.IsMatch(pan, pattern);
        }

        public static bool IsValidAadhaar(string aadhaar)
        {
            if (string.IsNullOrWhiteSpace(aadhaar))
                return false;

            // Aadhaar pattern: 12 digits
            string pattern = @"^[0-9]{12}$";
            return Regex.IsMatch(aadhaar, pattern);
        }
    }
}