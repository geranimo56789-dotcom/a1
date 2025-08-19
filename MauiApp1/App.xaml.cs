using MauiApp1.Services;

namespace MauiApp1;

public partial class App : Application
{
    public App()
    {
        InitializeComponent();
        MainPage = new AppShell();
        ApplySavedLanguage();
        
        // Navigate to login initially
        Shell.Current.GoToAsync("//login");
    }

    private void ApplySavedLanguage()
    {
        var savedLanguage = Preferences.Get("app_language", "en");
        LocalizationService.Instance.SetLanguage(savedLanguage);
    }
}