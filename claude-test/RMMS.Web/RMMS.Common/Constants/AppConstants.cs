// RMMS.Common/Constants/AppConstants.cs
namespace RMMS.Common.Constants
{
    public static class AppConstants
    {
        public static class Roles
        {
            public const string Admin = "Admin";
            public const string Manager = "Manager";
            public const string Operator = "Operator";
            public const string Viewer = "Viewer";
        }

        public static class PaymentStatus
        {
            public const string Pending = "Pending";
            public const string Partial = "Partial";
            public const string Paid = "Paid";
            public const string Overdue = "Overdue";
            public const string Cancelled = "Cancelled";
        }

        public static class TransactionType
        {
            public const string Sale = "Sale";
            public const string Purchase = "Purchase";
            public const string Payment = "Payment";
            public const string Receipt = "Receipt";
            public const string Journal = "Journal";
            public const string Contra = "Contra";
        }

        public static class AssetStatus
        {
            public const string Active = "Active";
            public const string Inactive = "Inactive";
            public const string Disposed = "Disposed";
            public const string UnderMaintenance = "Under Maintenance";
        }

        public static class GSTRates
        {
            public const decimal Rice = 5.0m;
            public const decimal ByProducts = 5.0m;
            public const decimal Services = 18.0m;
        }
    }
}