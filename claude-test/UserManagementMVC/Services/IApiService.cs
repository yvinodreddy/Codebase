using UserManagementMVC.Models;

namespace UserManagementMVC.Services;

public interface IApiService
{
    Task<UserDto?> RegisterAsync(string username, string email, string password, string firstName, string lastName);
    Task<LoginResponseDto?> LoginAsync(string username, string password);
}
