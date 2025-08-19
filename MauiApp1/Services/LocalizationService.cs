using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace MauiApp1.Services
{
    public class LocalizationService : INotifyPropertyChanged
    {
        private static LocalizationService? _instance;
        public static LocalizationService Instance => _instance ??= new LocalizationService();

        private readonly Dictionary<string, Dictionary<string, string>> _translations = new()
        {
            ["en"] = new Dictionary<string, string>
            {
                ["Menu"] = "Menu",
                ["Home"] = "Home",
                ["Check_Predictions"] = "Check Predictions",
                ["Settings"] = "Settings",
                ["Game_Rules"] = "Game Rules",
                ["Admin_Panel"] = "Admin Panel",
                ["Log_out"] = "Log out",
                ["Change_Password"] = "Change password",
                ["Change_Language"] = "Change Language",
                ["Update_Email"] = "Update Email",
                ["Delete_Account"] = "Delete Account",
                ["App_Title"] = "VAR6 Betting App",
                ["Email"] = "Email",
                ["Password"] = "Password",
                ["Remember_Me"] = "Remember me",
                ["Sign_In"] = "Sign In",
                ["Create_Account"] = "Create Account"
            },
            ["fr"] = new Dictionary<string, string>
            {
                ["Menu"] = "Menu",
                ["Home"] = "Accueil",
                ["Check_Predictions"] = "Vérifier les Prédictions",
                ["Settings"] = "Paramètres",
                ["Game_Rules"] = "Règles du Jeu",
                ["Admin_Panel"] = "Panneau Admin",
                ["Log_out"] = "Se déconnecter",
                ["Change_Password"] = "Changer le mot de passe",
                ["Change_Language"] = "Changer la langue",
                ["Update_Email"] = "Mettre à jour l'email",
                ["Delete_Account"] = "Supprimer le compte",
                ["App_Title"] = "Application de Paris VAR6",
                ["Email"] = "Email",
                ["Password"] = "Mot de passe",
                ["Remember_Me"] = "Se souvenir de moi",
                ["Sign_In"] = "Se connecter",
                ["Create_Account"] = "Créer un compte"
            }
        };

        private string _currentLanguage = "en";

        public string CurrentLanguage
        {
            get => _currentLanguage;
            set
            {
                if (_currentLanguage != value)
                {
                    _currentLanguage = value;
                    OnPropertyChanged();
                    OnPropertyChanged(nameof(CurrentLanguage));
                    // Notify all string properties to update
                    OnPropertyChanged(nameof(MenuText));
                    OnPropertyChanged(nameof(HomeText));
                    OnPropertyChanged(nameof(CheckPredictionsText));
                    OnPropertyChanged(nameof(SettingsText));
                    OnPropertyChanged(nameof(GameRulesText));
                    OnPropertyChanged(nameof(AdminPanelText));
                    OnPropertyChanged(nameof(LogOutText));
                    OnPropertyChanged(nameof(ChangePasswordText));
                    OnPropertyChanged(nameof(ChangeLanguageText));
                    OnPropertyChanged(nameof(UpdateEmailText));
                    OnPropertyChanged(nameof(DeleteAccountText));
                    OnPropertyChanged(nameof(AppTitleText));
                    OnPropertyChanged(nameof(EmailText));
                    OnPropertyChanged(nameof(PasswordText));
                    OnPropertyChanged(nameof(RememberMeText));
                    OnPropertyChanged(nameof(SignInText));
                    OnPropertyChanged(nameof(CreateAccountText));
                }
            }
        }

        // Properties for direct binding
        public string MenuText => GetString("Menu");
        public string HomeText => GetString("Home");
        public string CheckPredictionsText => GetString("Check_Predictions");
        public string SettingsText => GetString("Settings");
        public string GameRulesText => GetString("Game_Rules");
        public string AdminPanelText => GetString("Admin_Panel");
        public string LogOutText => GetString("Log_out");
        public string ChangePasswordText => GetString("Change_Password");
        public string ChangeLanguageText => GetString("Change_Language");
        public string UpdateEmailText => GetString("Update_Email");
        public string DeleteAccountText => GetString("Delete_Account");
        public string AppTitleText => GetString("App_Title");
        public string EmailText => GetString("Email");
        public string PasswordText => GetString("Password");
        public string RememberMeText => GetString("Remember_Me");
        public string SignInText => GetString("Sign_In");
        public string CreateAccountText => GetString("Create_Account");

        public string GetString(string key)
        {
            if (_translations.TryGetValue(_currentLanguage, out var langDict) && 
                langDict.TryGetValue(key, out var value))
            {
                return value;
            }
            
            // Fallback to English
            if (_translations["en"].TryGetValue(key, out var fallback))
            {
                return fallback;
            }
            
            return key; // Return key if not found
        }

        public void SetLanguage(string language)
        {
            if (_translations.ContainsKey(language))
            {
                CurrentLanguage = language;
                Preferences.Set("app_language", language);
            }
        }

        public event PropertyChangedEventHandler? PropertyChanged;

        protected virtual void OnPropertyChanged([CallerMemberName] string? propertyName = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}
