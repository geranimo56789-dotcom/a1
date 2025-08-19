using MauiApp1.Services;
using MauiApp1.Models;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Windows.Input;
using System.Collections.ObjectModel;
using Microsoft.Maui.ApplicationModel;
using Microsoft.Maui.Storage;

namespace MauiApp1.ViewModels
{
    public class BaseViewModel : INotifyPropertyChanged
    {
        public event PropertyChangedEventHandler? PropertyChanged;
        protected virtual void OnPropertyChanged([CallerMemberName] string? propertyName = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }

    public class LoginViewModel : BaseViewModel
    {
        private readonly AuthService _authService;
        private string _email = string.Empty;
        private string _password = string.Empty;
        private bool _isLoading;
        private bool _rememberMe;

        public string Email
        {
            get => _email;
            set { _email = value; OnPropertyChanged(); }
        }

        public string Password
        {
            get => _password;
            set { _password = value; OnPropertyChanged(); }
        }

        public bool IsLoading
        {
            get => _isLoading;
            set { _isLoading = value; OnPropertyChanged(); }
        }

        public bool RememberMe
        {
            get => _rememberMe;
            set { _rememberMe = value; OnPropertyChanged(); Preferences.Set("remember_me", value); }
        }

        public ICommand SignInCommand { get; }
        public ICommand CreateAccountCommand { get; }

        public LoginViewModel(AuthService authService)
        {
            _authService = authService;
            SignInCommand = new Command(async () => await SignInAsync());
            CreateAccountCommand = new Command(async () => await CreateAccountAsync());
            // Load stored credentials
            RememberMe = Preferences.Get("remember_me", false);
            if (RememberMe)
            {
                MainThread.BeginInvokeOnMainThread(async () =>
                {
                    try
                    {
                        Email = await SecureStorage.GetAsync("email") ?? Email;
                        var storedPass = await SecureStorage.GetAsync("password");
                        if (!string.IsNullOrEmpty(Email) && !string.IsNullOrEmpty(storedPass))
                        {
                            Password = storedPass;
                            await SignInAsync();
                        }
                    }
                    catch { }
                });
            }
        }

        private async Task SignInAsync()
        {
            try
            {
                IsLoading = true;
                var user = await _authService.SignInWithEmailAndPasswordAsync(Email, Password);
                if (RememberMe)
                {
                    try { await SecureStorage.SetAsync("email", Email); } catch { }
                    try { await SecureStorage.SetAsync("password", Password); } catch { }
                }
                
                // Show admin menu if user is admin
                if (user.IsAdmin && Application.Current.MainPage is AppShell shell)
                {
                    shell.ShowAdminMenu(true);
                    await Shell.Current.GoToAsync("//admin");
                }
                else
                {
                    await Shell.Current.GoToAsync("//home");
                }
            }
            catch (Exception ex)
            {
                if (Application.Current?.MainPage != null)
                    await Application.Current.MainPage.DisplayAlert("Login Failed", ex.Message, "OK");
            }
            finally
            {
                IsLoading = false;
            }
        }

        private async Task CreateAccountAsync()
        {
            try
            {
                IsLoading = true;
                var user = await _authService.CreateUserWithEmailAndPasswordAsync(Email, Password);
                await Shell.Current.GoToAsync("//home");
            }
            catch (Exception ex)
            {
                if (Application.Current?.MainPage != null)
                    await Application.Current.MainPage.DisplayAlert("Sign Up Failed", ex.Message, "OK");
            }
            finally
            {
                IsLoading = false;
            }
        }
    }

    public class HomeViewModel : BaseViewModel
    {
        private readonly AuthService _authService;
        private readonly SupabaseService _firestoreService;
        private bool _isLoading;

        public ObservableCollection<MatchViewModel> TodaysMatches { get; } = new();
        public ObservableCollection<PredictionViewModel> UserPredictions { get; } = new();

        public bool IsLoading
        {
            get => _isLoading;
            set { _isLoading = value; OnPropertyChanged(); }
        }

        public string UserEmail => _authService.CurrentUser?.Email ?? "Not signed in";

        public ICommand LoadDataCommand { get; }
        public ICommand SubmitPredictionsCommand { get; }
        public ICommand SignOutCommand { get; }

        public HomeViewModel(AuthService authService, SupabaseService firestoreService)
        {
            _authService = authService;
            _firestoreService = firestoreService;
            LoadDataCommand = new Command(async () => await LoadDataAsync());
            SubmitPredictionsCommand = new Command(async () => await SubmitPredictionsAsync());
            SignOutCommand = new Command(async () => await SignOutAsync());
        }

        public async Task LoadDataAsync()
        {
            try
            {
                IsLoading = true;
                var matches = await _firestoreService.GetMatchesAsync();
                
                TodaysMatches.Clear();
                foreach (var match in matches)
                {
                    var vm = new MatchViewModel(match, _firestoreService);
                    TodaysMatches.Add(vm);
                }

                if (_authService.CurrentUser != null)
                {
                    var predictions = await _firestoreService.GetPredictionsAsync(_authService.CurrentUser.Uid);
                    UserPredictions.Clear();
                    foreach (var prediction in predictions)
                    {
                        UserPredictions.Add(new PredictionViewModel(prediction, _firestoreService));
                    }
                }
            }
            catch (Exception ex)
            {
                if (Application.Current?.MainPage != null)
                    await Application.Current.MainPage.DisplayAlert("Error", ex.Message, "OK");
            }
            finally
            {
                IsLoading = false;
            }
        }

        private async Task SubmitPredictionsAsync()
        {
            try
            {
                var predictions = TodaysMatches.Where(m => m.HasPrediction).ToList();
                if (!predictions.Any())
                {
                    if (Application.Current?.MainPage != null)
                        await Application.Current.MainPage.DisplayAlert("Error", "Please make at least one prediction", "OK");
                    return;
                }

                IsLoading = true;
                foreach (var match in predictions)
                {
                    var prediction = new Prediction
                    {
                        MatchId = match.Match.MatchId,
                        HomeScore = match.HomePrediction,
                        AwayScore = match.AwayPrediction,
                        HomeTeam = match.Match.HomeTeam,
                        AwayTeam = match.Match.AwayTeam,
                        HomeTeamCode = match.Match.HomeTeamCode,
                        AwayTeamCode = match.Match.AwayTeamCode,
                        CreatedAt = DateTimeOffset.Now.ToUnixTimeSeconds(),
                        LockAt = match.Match.TimeUtc
                    };

                    if (_authService.CurrentUser != null)
                        await _firestoreService.SubmitPredictionAsync(_authService.CurrentUser.Uid, prediction);
                }

                if (Application.Current?.MainPage != null)
                    await Application.Current.MainPage.DisplayAlert("Success", "Predictions submitted!", "OK");
                await LoadDataAsync();
            }
            catch (Exception ex)
            {
                if (Application.Current?.MainPage != null)
                    await Application.Current.MainPage.DisplayAlert("Error", ex.Message, "OK");
            }
            finally
            {
                IsLoading = false;
            }
        }

        private async Task SignOutAsync()
        {
            await _authService.SignOutAsync();
            await Shell.Current.GoToAsync("//login");
        }
    }

    public class MatchViewModel : BaseViewModel
    {
        public Match Match { get; }
        public TeamInfo HomeTeamInfo { get; }
        public TeamInfo AwayTeamInfo { get; }
        public string HomeLogoPath => $"{Match.HomeTeamCode.ToLower()}.png";
        public string AwayLogoPath => $"{Match.AwayTeamCode.ToLower()}.png";
        
        private int _homePrediction;
        private int _awayPrediction;

        public int HomePrediction
        {
            get => _homePrediction;
            set { _homePrediction = Math.Max(0, Math.Min(10, value)); OnPropertyChanged(); OnPropertyChanged(nameof(HasPrediction)); }
        }

        public int AwayPrediction
        {
            get => _awayPrediction;
            set { _awayPrediction = Math.Max(0, Math.Min(10, value)); OnPropertyChanged(); OnPropertyChanged(nameof(HasPrediction)); }
        }

        public bool HasPrediction => HomePrediction >= 0 && AwayPrediction >= 0;
        public bool IsUpcoming => DateTimeOffset.FromUnixTimeSeconds(Match.TimeUtc) > DateTimeOffset.Now;
        public string MatchTime => DateTimeOffset.FromUnixTimeSeconds(Match.TimeUtc).ToString("HH:mm");

        public ICommand IncreaseHomeScoreCommand { get; }
        public ICommand DecreaseHomeScoreCommand { get; }
        public ICommand IncreaseAwayScoreCommand { get; }
        public ICommand DecreaseAwayScoreCommand { get; }

        public MatchViewModel(Match match, SupabaseService firestoreService)
        {
            Match = match;
            HomeTeamInfo = firestoreService.GetTeamInfo(match.HomeTeamCode);
            AwayTeamInfo = firestoreService.GetTeamInfo(match.AwayTeamCode);

            IncreaseHomeScoreCommand = new Command(() => { if (IsUpcoming && HomePrediction < 10) HomePrediction++; });
            DecreaseHomeScoreCommand = new Command(() => { if (IsUpcoming && HomePrediction > 0) HomePrediction--; });
            IncreaseAwayScoreCommand = new Command(() => { if (IsUpcoming && AwayPrediction < 10) AwayPrediction++; });
            DecreaseAwayScoreCommand = new Command(() => { if (IsUpcoming && AwayPrediction > 0) AwayPrediction--; });
        }
    }

    public class PredictionViewModel : BaseViewModel
    {
        public Prediction Prediction { get; }
        public TeamInfo HomeTeamInfo { get; }
        public TeamInfo AwayTeamInfo { get; }
        public string HomeLogoPath => $"{Prediction.HomeTeamCode.ToLower()}.png";
        public string AwayLogoPath => $"{Prediction.AwayTeamCode.ToLower()}.png";

        public string DisplayText => $"{Prediction.HomeTeam} {Prediction.HomeScore} - {Prediction.AwayScore} {Prediction.AwayTeam}";

        public PredictionViewModel(Prediction prediction, SupabaseService firestoreService)
        {
            Prediction = prediction;
            HomeTeamInfo = firestoreService.GetTeamInfo(prediction.HomeTeamCode);
            AwayTeamInfo = firestoreService.GetTeamInfo(prediction.AwayTeamCode);
        }
    }

    public class AdminViewModel : BaseViewModel
    {
        private readonly AuthService _authService;
        private readonly SupabaseService _firestoreService;

        public ICommand SignOutCommand { get; }
        public ICommand AddMatchCommand { get; }
        public ICommand ExportWinningBetsCommand { get; }

        // Properties for form inputs
        public string Date { get; set; } = string.Empty;
        public string Hour { get; set; } = string.Empty;
        public string Team1 { get; set; } = string.Empty;
        public string Team2 { get; set; } = string.Empty;

        public AdminViewModel(AuthService authService, SupabaseService firestoreService)
        {
            _authService = authService;
            _firestoreService = firestoreService;
            SignOutCommand = new Command(async () => await SignOutAsync());
            AddMatchCommand = new Command(async () => await AddMatchAsync());
            ExportWinningBetsCommand = new Command(async () => await ExportWinningBetsAsync());
        }

        private async Task AddMatchAsync()
        {
            try
            {
                if (string.IsNullOrEmpty(Date) || string.IsNullOrEmpty(Hour) || 
                    string.IsNullOrEmpty(Team1) || string.IsNullOrEmpty(Team2))
                {
                    if (Application.Current?.MainPage != null)
                        await Application.Current.MainPage.DisplayAlert("Error", "Please fill all fields", "OK");
                    return;
                }

                var success = await _firestoreService.AddMatchAsync(Team1, Team2, Date, Hour);
                if (success)
                {
                    if (Application.Current?.MainPage != null)
                        await Application.Current.MainPage.DisplayAlert("Success", "Match added successfully!", "OK");
                    // Clear form
                    Date = Hour = Team1 = Team2 = string.Empty;
                    OnPropertyChanged(nameof(Date));
                    OnPropertyChanged(nameof(Hour));
                    OnPropertyChanged(nameof(Team1));
                    OnPropertyChanged(nameof(Team2));
                }
                else
                {
                    if (Application.Current?.MainPage != null)
                        await Application.Current.MainPage.DisplayAlert("Error", "Failed to add match", "OK");
                }
            }
            catch (Exception ex)
            {
                if (Application.Current?.MainPage != null)
                    await Application.Current.MainPage.DisplayAlert("Error", ex.Message, "OK");
            }
        }

        private async Task SignOutAsync()
        {
            await _authService.SignOutAsync();
            await Shell.Current.GoToAsync("//login");
        }

        private async Task ExportWinningBetsAsync()
        {
            try
            {
                var winningBets = await _firestoreService.GetWinningBetsAsync();
                
                if (!winningBets.Any())
                {
                    if (Application.Current?.MainPage != null)
                        await Application.Current.MainPage.DisplayAlert("No Data", "No winning bets found to export.", "OK");
                    return;
                }

                // Create CSV content
                var csvContent = "Match ID,Home Team,Away Team,Home Score,Away Score,User Email,Home Prediction,Away Prediction\n";
                
                foreach (var bet in winningBets)
                {
                    csvContent += $"{bet.MatchId},{bet.HomeTeam},{bet.AwayTeam},{bet.HomeScore},{bet.AwayScore},{bet.UserEmail},{bet.HomePrediction},{bet.AwayPrediction}\n";
                }

                // Get desktop path for Windows
                var desktopPath = Environment.GetFolderPath(Environment.SpecialFolder.Desktop);
                var fileName = $"winning_bets_{DateTime.Now:yyyyMMdd_HHmmss}.csv";
                var filePath = Path.Combine(desktopPath, fileName);

                // Write to file
                await File.WriteAllTextAsync(filePath, csvContent);

                if (Application.Current?.MainPage != null)
                    await Application.Current.MainPage.DisplayAlert("Export Successful", 
                        $"Winning bets exported to: {fileName}\nLocation: {desktopPath}", "OK");
            }
            catch (Exception ex)
            {
                if (Application.Current?.MainPage != null)
                    await Application.Current.MainPage.DisplayAlert("Export Failed", ex.Message, "OK");
            }
        }
    }
}
