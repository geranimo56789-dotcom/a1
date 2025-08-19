using MauiApp1.Services;
using MauiApp1.Views;

namespace MauiApp1;

public partial class AppShell : Shell
{
    private readonly AuthService _authService;

    public AppShell()
    {
        InitializeComponent();
        _authService = ServiceHelper.GetService<AuthService>();

        // Explicit route registrations
        Routing.RegisterRoute("login", typeof(LoginPage));
        Routing.RegisterRoute("home", typeof(HomePage));
        Routing.RegisterRoute("predictions", typeof(PredictionsPage));
        Routing.RegisterRoute("settings", typeof(SettingsPage));
        Routing.RegisterRoute("gamerules", typeof(GameRulesPage));
        Routing.RegisterRoute("admin", typeof(AdminPage));
        Routing.RegisterRoute("logout", typeof(LogoutPage));
    }

    private async void OnLogoutClicked(object sender, EventArgs e)
    {
        await _authService.SignOutAsync();
        await Shell.Current.GoToAsync("//login");
    }

    public void ShowAdminMenu(bool show)
    {
        AdminMenuItem.IsVisible = show;
    }
}

public static class ServiceHelper
{
    public static T GetService<T>() => Current.GetService<T>();

    public static IServiceProvider Current =>
#if WINDOWS10_0_17763_0_OR_GREATER
        MauiWinUIApplication.Current.Services;
#elif ANDROID
        MauiApplication.Current.Services;
#elif IOS || MACCATALYST
        MauiUIApplicationDelegate.Current.Services;
#else
        null;
#endif
}