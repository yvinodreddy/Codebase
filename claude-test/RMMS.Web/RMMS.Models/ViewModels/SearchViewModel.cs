// RMMS.Models/ViewModels/SearchViewModel.cs
namespace RMMS.Models.ViewModels
{
    public class SearchViewModel
    {
        public string? SearchTerm { get; set; }
        public DateTime? StartDate { get; set; }
        public DateTime? EndDate { get; set; }
        public string? Category { get; set; }
        public string? Status { get; set; }
    }
}