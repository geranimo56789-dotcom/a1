using MauiApp1.ViewModels;

namespace MauiApp1.Views;

public partial class LoginPage : ContentPage
{
	public LoginPage(LoginViewModel viewModel)
	{
		InitializeComponent();
		BindingContext = viewModel;
	}

	private void OnEmailCompleted(object sender, EventArgs e)
	{
		PasswordEntry?.Focus();
	}

	private void OnPasswordCompleted(object sender, EventArgs e)
	{
		if (BindingContext is LoginViewModel vm && vm.SignInCommand.CanExecute(null))
			vm.SignInCommand.Execute(null);
	}
}

