namespace MauiApp1.Views;

using MauiApp1.Services;

public partial class SettingsPage : ContentPage
{
    private readonly AuthService _auth;

    public SettingsPage()
    {
        InitializeComponent();
        _auth = ServiceHelper.GetService<AuthService>();
        BindingContext = LocalizationService.Instance;
    }

    private async void OnBackClicked(object sender, EventArgs e)
    {
        await Shell.Current.GoToAsync("..");
    }

    private async void OnChangePasswordClicked(object sender, EventArgs e)
    {
        try
        {
            string newPass = await DisplayPromptAsync("Change password", "Enter a new password", "Update", "Cancel", "New password", -1, Keyboard.Text, "") ?? string.Empty;
            newPass = newPass.Trim();
            if (string.IsNullOrEmpty(newPass))
            {
                await DisplayAlert("Error", "Enter a new password", "OK");
                return;
            }
            await _auth.ChangePasswordAsync(newPass);
            await DisplayAlert("Success", "Password updated", "OK");
        }
        catch (Exception ex)
        {
            await DisplayAlert("Error", ex.Message, "OK");
        }
    }

    private async void OnDeleteAccountClicked(object sender, EventArgs e)
    {
        var confirm = await DisplayAlert("Confirm", "Delete your account? This cannot be undone.", "Delete", "Cancel");
        if (!confirm) return;
        try
        {
            await _auth.DeleteAccountAsync();
            await DisplayAlert("Deleted", "Your account was deleted", "OK");
            await Shell.Current.GoToAsync("//login");
        }
        catch (Exception ex)
        {
            await DisplayAlert("Error", ex.Message, "OK");
        }
    }

    private async void OnLanguageClicked(object sender, EventArgs e)
    {
        string action = await DisplayActionSheet("Select Language", "Cancel", null, "English", "Français");
        if (action == "Français")
        {
            LocalizationService.Instance.SetLanguage("fr");
            await DisplayAlert("Langue", "Français sélectionné!", "OK");
        }
        else if (action == "English")
        {
            LocalizationService.Instance.SetLanguage("en");
            await DisplayAlert("Language", "English selected!", "OK");
        }
    }

    private async void OnUpdateEmailClicked(object sender, EventArgs e)
    {
        try
        {
            string newEmail = await DisplayPromptAsync("Update Email", "Enter new email address", "Update", "Cancel", "New email", -1, Keyboard.Email, "") ?? string.Empty;
            newEmail = newEmail.Trim();
            if (string.IsNullOrEmpty(newEmail))
            {
                await DisplayAlert("Error", "Enter a valid email", "OK");
                return;
            }
            await DisplayAlert("Success", $"Email updated to {newEmail}", "OK");
        }
        catch (Exception ex)
        {
            await DisplayAlert("Error", ex.Message, "OK");
        }
    }



    private void OnMenuClicked(object sender, EventArgs e)
    {
        Shell.Current.FlyoutIsPresented = true;
    }

    private async void OnLogoutClicked(object sender, EventArgs e)
    {
        await _auth.SignOutAsync();
        await Shell.Current.GoToAsync("//login");
    }
}
