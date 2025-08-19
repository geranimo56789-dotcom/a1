using MauiApp1.Services;

namespace MauiApp1.Views;

public partial class LogoutPage : ContentPage
{
    private readonly AuthService _auth;

    public LogoutPage()
    {
        InitializeComponent();
        _auth = ServiceHelper.GetService<AuthService>();
    }

    protected override async void OnAppearing()
    {
        base.OnAppearing();
        
        // Perform logout
        await _auth.SignOutAsync();
        
        // Navigate back to login
        await Shell.Current.GoToAsync("//login");
    }
}
