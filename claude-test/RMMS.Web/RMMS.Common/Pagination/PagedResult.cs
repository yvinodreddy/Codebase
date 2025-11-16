using System;
using System.Collections.Generic;
using System.Linq;

namespace RMMS.Common.Pagination
{
    public class PagedResult<T>
    {
        public List<T> Items { get; set; } = new List<T>();
        public int CurrentPage { get; set; }
        public int PageSize { get; set; }
        public int TotalPages { get; set; }
        public int TotalItems { get; set; }
        public bool HasPreviousPage => CurrentPage > 1;
        public bool HasNextPage => CurrentPage < TotalPages;
        public string? SortBy { get; set; }
        public string? SortOrder { get; set; }

        public PagedResult()
        {
        }

        public PagedResult(List<T> items, int count, int pageNumber, int pageSize, string? sortBy = null, string? sortOrder = null)
        {
            Items = items;
            TotalItems = count;
            CurrentPage = pageNumber;
            PageSize = pageSize;
            TotalPages = (int)Math.Ceiling(count / (double)pageSize);
            SortBy = sortBy;
            SortOrder = sortOrder;
        }

        public static PagedResult<T> Create(IQueryable<T> source, int pageNumber, int pageSize, string? sortBy = null, string? sortOrder = null)
        {
            var count = source.Count();
            var items = source.Skip((pageNumber - 1) * pageSize).Take(pageSize).ToList();
            return new PagedResult<T>(items, count, pageNumber, pageSize, sortBy, sortOrder);
        }

        public static PagedResult<T> Create(IEnumerable<T> source, int pageNumber, int pageSize, string? sortBy = null, string? sortOrder = null)
        {
            var sourceList = source.ToList();
            var count = sourceList.Count;
            var items = sourceList.Skip((pageNumber - 1) * pageSize).Take(pageSize).ToList();
            return new PagedResult<T>(items, count, pageNumber, pageSize, sortBy, sortOrder);
        }
    }
}
