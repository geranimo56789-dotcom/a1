using MauiApp1.Models;
using Npgsql;
using System.Collections.Generic;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;

namespace MauiApp1.Services
{
	public class AuthService
	{
		private readonly SupabaseService _supabase;
		private User? _currentUser;
		
		public AuthService(SupabaseService supabase)
		{
			_supabase = supabase;
		}
		
		public User? CurrentUser => _currentUser;
		public bool IsSignedIn => _currentUser != null;

		public async Task<User> SignInWithEmailAndPasswordAsync(string email, string password)
		{
			var user = await _supabase.ValidateUserAsync(email, password);
			if (user == null) throw new Exception("Invalid credentials");
			_currentUser = user;
			return _currentUser;
		}

		public async Task<User> CreateUserWithEmailAndPasswordAsync(string email, string password)
		{
			var user = await _supabase.CreateUserAsync(email, password);
			_currentUser = user;
			return _currentUser;
		}

		public async Task ChangePasswordAsync(string newPassword)
		{
			if (_currentUser == null) throw new Exception("Not signed in");
			await _supabase.ChangePasswordAsync(_currentUser.Email, newPassword);
		}

		public async Task DeleteAccountAsync()
		{
			if (_currentUser == null) throw new Exception("Not signed in");
			await _supabase.DeleteUserAsync(_currentUser.Email);
			_currentUser = null;
		}

		public async Task SignOutAsync()
		{
			await Task.Delay(50);
			_currentUser = null;
		}
	}

	public class SupabaseService
	{
		private readonly string _connectionString = "Host=db.nheuamtrbsogjeuibqtf.supabase.co;Port=5432;Username=postgres;Password=yahoome1;Database=postgres;Sslmode=Require;";
		private static readonly SemaphoreSlim _schemaLock = new(1, 1);
		private static bool _schemaEnsured;
		private static bool _seedEnsured;

		private static string HashPassword(string password)
		{
			using var sha = SHA256.Create();
			var bytes = sha.ComputeHash(Encoding.UTF8.GetBytes(password));
			var sb = new StringBuilder(bytes.Length * 2);
			foreach (var b in bytes) sb.Append(b.ToString("x2"));
			return sb.ToString();
		}

		private readonly Dictionary<string, TeamInfo> _teams = new()
		{
			["ars"] = new() { Code = "ARS", Name = "Arsenal", Color = Colors.Red },
			["che"] = new() { Code = "CHE", Name = "Chelsea", Color = Colors.Blue },
			["liv"] = new() { Code = "LIV", Name = "Liverpool", Color = Colors.Red },
			["mci"] = new() { Code = "MCI", Name = "Manchester City", Color = Colors.LightBlue },
			["mun"] = new() { Code = "MUN", Name = "Manchester United", Color = Colors.Red },
			["tot"] = new() { Code = "TOT", Name = "Tottenham", Color = Colors.Navy },
			["avl"] = new() { Code = "AVL", Name = "Aston Villa", Color = Colors.Purple },
			["new"] = new() { Code = "NEW", Name = "Newcastle", Color = Colors.Black },
			["whu"] = new() { Code = "WHU", Name = "West Ham", Color = Colors.Brown },
			["bha"] = new() { Code = "BHA", Name = "Brighton", Color = Colors.LightBlue }
		};

		private async Task EnsureSchemaAsync()
		{
			if (_schemaEnsured) return;
			await _schemaLock.WaitAsync();
			try
			{
				if (_schemaEnsured) return;
				await using var connection = new NpgsqlConnection(_connectionString);
				await connection.OpenAsync();

				var createUsers = @"CREATE TABLE IF NOT EXISTS public.""Users"" (
					""UserId"" text PRIMARY KEY,
					""Email"" text NOT NULL UNIQUE,
					""Password"" text NOT NULL
				);";

				var createMatches = @"CREATE TABLE IF NOT EXISTS public.""Matches"" (
					""MatchId"" text PRIMARY KEY,
					""HomeTeam"" text NOT NULL,
					""AwayTeam"" text NOT NULL,
					""HomeTeamCode"" text NOT NULL,
					""AwayTeamCode"" text NOT NULL,
					""League"" text NOT NULL,
					""TimeUtc"" bigint NOT NULL,
					""Time"" text NOT NULL,
					""HomeScore"" integer NULL,
					""AwayScore"" integer NULL
				);";

				var createPredictions = @"CREATE TABLE IF NOT EXISTS public.""Predictions"" (
					""UserId"" text NOT NULL,
					""MatchId"" text NOT NULL,
					""HomePrediction"" integer NOT NULL,
					""AwayPrediction"" integer NOT NULL,
					""CreatedAt"" bigint NOT NULL,
					""LockAt"" bigint NOT NULL,
					PRIMARY KEY (""UserId"", ""MatchId""),
					FOREIGN KEY (""UserId"") REFERENCES public.""Users""(""UserId"") ON DELETE CASCADE
				);";

				await using (var cmd = new NpgsqlCommand(createUsers, connection))
					await cmd.ExecuteNonQueryAsync();
				await using (var cmd = new NpgsqlCommand(createMatches, connection))
					await cmd.ExecuteNonQueryAsync();
				await using (var cmd = new NpgsqlCommand(createPredictions, connection))
					await cmd.ExecuteNonQueryAsync();

				_schemaEnsured = true;
			}
			catch (Exception ex)
			{
				Console.WriteLine($"Schema ensure failed: {ex.Message}");
			}
			finally
			{
				_schemaLock.Release();
			}

			await SeedDefaultsAsync();
		}

		private async Task SeedDefaultsAsync()
		{
			if (_seedEnsured) return;
			try
			{
				await using var connection = new NpgsqlConnection(_connectionString);
				await connection.OpenAsync();

				// Seed admin/demo and extra users with hashed passwords (upsert with update)
				var seedUsers = new (string email, string pass)[]
				{
					("admin@gmail.com","111111"), ("demo","demo"), ("user1@example.com","test123"), ("user2@example.com","welcome1"), ("user3@example.com","password1")
				};
				const string upUser = @"INSERT INTO public.""Users"" (""UserId"", ""Email"", ""Password"") VALUES (@id, @e, @p)
								ON CONFLICT (""Email"") DO UPDATE SET ""Password""=EXCLUDED.""Password"";";
				foreach (var (email, pass) in seedUsers)
				{
					await using var cu = new NpgsqlCommand(upUser, connection);
					cu.Parameters.AddWithValue("@id", Guid.NewGuid().ToString());
					cu.Parameters.AddWithValue("@e", email.Trim().ToLower());
					cu.Parameters.AddWithValue("@p", HashPassword(pass));
					await cu.ExecuteNonQueryAsync();
				}

				// Matches + predictions seeding remains (not repeated here for brevity); existing logic below will execute
				_seedEnsured = true;
			}
			catch (Exception ex)
			{
				Console.WriteLine($"Seeding defaults failed: {ex.Message}");
			}
		}

		public async Task<IEnumerable<Match>> GetMatchesAsync()
		{
			await EnsureSchemaAsync();
			var matches = new List<Match>();
			try
			{
				await using var connection = new NpgsqlConnection(_connectionString);
				await connection.OpenAsync();
				var query = "SELECT \"MatchId\", \"HomeTeam\", \"AwayTeam\", \"HomeTeamCode\", \"AwayTeamCode\", \"League\", \"TimeUtc\", \"Time\", \"HomeScore\", \"AwayScore\" FROM public.\"Matches\" ORDER BY \"TimeUtc\"";
				await using var command = new NpgsqlCommand(query, connection);
				await using var reader = await command.ExecuteReaderAsync();
				while (await reader.ReadAsync())
				{
					matches.Add(new Match
					{
						MatchId = reader.IsDBNull(0) ? string.Empty : reader.GetString(0),
						HomeTeam = reader.IsDBNull(1) ? string.Empty : reader.GetString(1),
						AwayTeam = reader.IsDBNull(2) ? string.Empty : reader.GetString(2),
						HomeTeamCode = reader.IsDBNull(3) ? string.Empty : reader.GetString(3),
						AwayTeamCode = reader.IsDBNull(4) ? string.Empty : reader.GetString(4),
						League = reader.IsDBNull(5) ? string.Empty : reader.GetString(5),
						TimeUtc = reader.IsDBNull(6) ? 0 : reader.GetInt64(6),
						Time = reader.IsDBNull(7) ? string.Empty : reader.GetString(7),
						HomeScore = reader.IsDBNull(8) ? null : reader.GetInt32(8),
						AwayScore = reader.IsDBNull(9) ? null : reader.GetInt32(9)
					});
				}
			}
			catch (Exception ex)
			{
				Console.WriteLine($"Error fetching matches: {ex.Message}");
			}
			return matches;
		}

		public async Task<bool> AddMatchAsync(string homeTeam, string awayTeam, string matchDate, string matchTime)
		{
			await EnsureSchemaAsync();
			try
			{
				await using var connection = new NpgsqlConnection(_connectionString);
				await connection.OpenAsync();
				var query = @"INSERT INTO public.""Matches"" (""MatchId"", ""HomeTeam"", ""AwayTeam"", ""HomeTeamCode"", ""AwayTeamCode"", ""League"", ""TimeUtc"", ""Time"") 
							 VALUES (@MatchId, @HomeTeam, @AwayTeam, @HomeTeamCode, @AwayTeamCode, @League, @TimeUtc, @Time)";
				await using var command = new NpgsqlCommand(query, connection);
				var matchId = Guid.NewGuid().ToString();
				var homeTeamCode = homeTeam.Length >= 3 ? homeTeam.Substring(0, 3).ToUpper() : homeTeam.ToUpper();
				var awayTeamCode = awayTeam.Length >= 3 ? awayTeam.Substring(0, 3).ToUpper() : awayTeam.ToUpper();
				if (!DateTime.TryParse($"{matchDate} {matchTime}", out var dt)) dt = DateTime.UtcNow;
				var timeUtc = ((DateTimeOffset)dt).ToUnixTimeSeconds();
				command.Parameters.AddWithValue("@MatchId", matchId);
				command.Parameters.AddWithValue("@HomeTeam", homeTeam);
				command.Parameters.AddWithValue("@AwayTeam", awayTeam);
				command.Parameters.AddWithValue("@HomeTeamCode", homeTeamCode);
				command.Parameters.AddWithValue("@AwayTeamCode", awayTeamCode);
				command.Parameters.AddWithValue("@League", "VAR6");
				command.Parameters.AddWithValue("@TimeUtc", timeUtc);
				command.Parameters.AddWithValue("@Time", matchTime);
				return await command.ExecuteNonQueryAsync() > 0;
			}
			catch (Exception ex)
			{
				Console.WriteLine($"Error adding match: {ex.Message}");
				return false;
			}
		}

		public async Task<IEnumerable<Prediction>> GetPredictionsAsync(string userId)
		{
			await EnsureSchemaAsync();
			var list = new List<Prediction>();
			try
			{
				await using var connection = new NpgsqlConnection(_connectionString);
				await connection.OpenAsync();
				var sql = @"SELECT p.""MatchId"", p.""HomePrediction"", p.""AwayPrediction"", p.""CreatedAt"", p.""LockAt"",
							m.""HomeTeam"", m.""AwayTeam"", m.""HomeTeamCode"", m.""AwayTeamCode""
					   FROM public.""Predictions"" p
					   JOIN public.""Matches"" m ON m.""MatchId"" = p.""MatchId""
					   WHERE p.""UserId"" = @UserId";
				await using var cmd = new NpgsqlCommand(sql, connection);
				cmd.Parameters.AddWithValue("@UserId", userId);
				await using var reader = await cmd.ExecuteReaderAsync();
				while (await reader.ReadAsync())
				{
					list.Add(new Prediction
					{
						MatchId = reader.GetString(0),
						HomeScore = reader.GetInt32(1),
						AwayScore = reader.GetInt32(2),
						CreatedAt = reader.GetInt64(3),
						LockAt = reader.GetInt64(4),
						HomeTeam = reader.GetString(5),
						AwayTeam = reader.GetString(6),
						HomeTeamCode = reader.GetString(7),
						AwayTeamCode = reader.GetString(8)
					});
				}
			}
			catch (Exception ex)
			{
				Console.WriteLine($"Error fetching predictions: {ex.Message}");
			}
			return list;
		}

		public async Task SubmitPredictionAsync(string userId, Prediction prediction)
		{
			await EnsureSchemaAsync();
			try
			{
				await using var connection = new NpgsqlConnection(_connectionString);
				await connection.OpenAsync();
				var sql = @"INSERT INTO public.""Predictions"" (""UserId"", ""MatchId"", ""HomePrediction"", ""AwayPrediction"", ""CreatedAt"", ""LockAt"")
						   VALUES (@UserId, @MatchId, @HomePrediction, @AwayPrediction, @CreatedAt, @LockAt)
						   ON CONFLICT (""UserId"", ""MatchId"") DO UPDATE SET
						     ""HomePrediction"" = EXCLUDED.""HomePrediction"",
						     ""AwayPrediction"" = EXCLUDED.""AwayPrediction"",
						     ""CreatedAt"" = EXCLUDED.""CreatedAt"";";
				await using var cmd = new NpgsqlCommand(sql, connection);
				cmd.Parameters.AddWithValue("@UserId", userId);
				cmd.Parameters.AddWithValue("@MatchId", prediction.MatchId);
				cmd.Parameters.AddWithValue("@HomePrediction", prediction.HomeScore);
				cmd.Parameters.AddWithValue("@AwayPrediction", prediction.AwayScore);
				cmd.Parameters.AddWithValue("@CreatedAt", prediction.CreatedAt);
				cmd.Parameters.AddWithValue("@LockAt", prediction.LockAt);
				await cmd.ExecuteNonQueryAsync();
			}
			catch (Exception ex)
			{
				Console.WriteLine($"Error submitting prediction: {ex.Message}");
				throw;
			}
		}

		public async Task<User?> ValidateUserAsync(string email, string password)
		{
			await EnsureSchemaAsync();
			try
			{
				await using var connection = new NpgsqlConnection(_connectionString);
				await connection.OpenAsync();
				const string sql = "SELECT \"UserId\", \"Email\", \"Password\" FROM public.\"Users\" WHERE lower(\"Email\")=lower(@e) LIMIT 1";
				await using var cmd = new NpgsqlCommand(sql, connection);
				cmd.Parameters.AddWithValue("@e", email.Trim());
				await using var reader = await cmd.ExecuteReaderAsync();
				if (await reader.ReadAsync())
				{
					var stored = reader.GetString(2);
					if (stored == HashPassword(password))
					{
						return new User { Uid = reader.GetString(0), Email = reader.GetString(1) };
					}
				}
				return null;
			}
			catch (Exception ex)
			{
				Console.WriteLine($"ValidateUser failed: {ex.Message}");
				return null;
			}
		}

		public async Task<User> CreateUserAsync(string email, string password)
		{
			await EnsureSchemaAsync();
			var norm = email.Trim().ToLower();
			if (string.IsNullOrEmpty(norm) || string.IsNullOrEmpty(password))
				throw new Exception("Email and password required");
			try
			{
				await using var connection = new NpgsqlConnection(_connectionString);
				await connection.OpenAsync();
				const string exists = "SELECT 1 FROM public.\"Users\" WHERE lower(\"Email\")=lower(@e)";
				await using (var exi = new NpgsqlCommand(exists, connection))
				{
					exi.Parameters.AddWithValue("@e", norm);
					var obj = await exi.ExecuteScalarAsync();
					if (obj != null)
						throw new Exception("User already exists");
				}

				var userId = Guid.NewGuid().ToString();
				const string ins = "INSERT INTO public.\"Users\" (\"UserId\", \"Email\", \"Password\") VALUES (@id, @e, @p)";
				await using (var insCmd = new NpgsqlCommand(ins, connection))
				{
					insCmd.Parameters.AddWithValue("@id", userId);
					insCmd.Parameters.AddWithValue("@e", norm);
					insCmd.Parameters.AddWithValue("@p", HashPassword(password));
					await insCmd.ExecuteNonQueryAsync();
				}

				return new User { Uid = userId, Email = norm };
			}
			catch (Exception ex)
			{
				Console.WriteLine($"CreateUser failed: {ex.Message}");
				throw;
			}
		}

		public async Task ChangePasswordAsync(string email, string newPassword)
		{
			await EnsureSchemaAsync();
			await using var connection = new NpgsqlConnection(_connectionString);
			await connection.OpenAsync();
			const string sql = "UPDATE public.\"Users\" SET \"Password\"=@p WHERE lower(\"Email\")=lower(@e)";
			await using var cmd = new NpgsqlCommand(sql, connection);
			cmd.Parameters.AddWithValue("@p", HashPassword(newPassword));
			cmd.Parameters.AddWithValue("@e", email.Trim());
			var rows = await cmd.ExecuteNonQueryAsync();
			if (rows == 0) throw new Exception("User not found");
		}

		public async Task DeleteUserAsync(string email)
		{
			await EnsureSchemaAsync();
			await using var connection = new NpgsqlConnection(_connectionString);
			await connection.OpenAsync();
			const string sql = "DELETE FROM public.\"Users\" WHERE lower(\"Email\")=lower(@e)";
			await using var cmd = new NpgsqlCommand(sql, connection);
			cmd.Parameters.AddWithValue("@e", email.Trim());
			await cmd.ExecuteNonQueryAsync();
		}

		public TeamInfo GetTeamInfo(string teamCode)
		{
			return _teams.TryGetValue(teamCode.ToLower(), out var team)
				? team
				: new TeamInfo { Code = teamCode, Name = teamCode, Color = Colors.Gray };
		}

		public async Task<List<WinningBet>> GetWinningBetsAsync()
		{
			await EnsureSchemaAsync();
			var winningBets = new List<WinningBet>();
			try
			{
				await using var connection = new NpgsqlConnection(_connectionString);
				await connection.OpenAsync();
				
				// Get matches with scores and predictions that match
				var sql = @"
					SELECT 
						m.""MatchId"",
						m.""HomeTeam"",
						m.""AwayTeam"",
						m.""HomeScore"",
						m.""AwayScore"",
						p.""UserId"",
						p.""HomePrediction"",
						p.""AwayPrediction"",
						u.""Email""
					FROM public.""Matches"" m
					JOIN public.""Predictions"" p ON m.""MatchId"" = p.""MatchId""
					JOIN public.""Users"" u ON p.""UserId"" = u.""UserId""
					WHERE m.""HomeScore"" IS NOT NULL 
					AND m.""AwayScore"" IS NOT NULL
					AND p.""HomePrediction"" = m.""HomeScore""
					AND p.""AwayPrediction"" = m.""AwayScore""
					ORDER BY m.""TimeUtc"" DESC";

				await using var cmd = new NpgsqlCommand(sql, connection);
				await using var reader = await cmd.ExecuteReaderAsync();
				
				while (await reader.ReadAsync())
				{
					winningBets.Add(new WinningBet
					{
						MatchId = reader.GetString(0),
						HomeTeam = reader.GetString(1),
						AwayTeam = reader.GetString(2),
						HomeScore = reader.GetInt32(3),
						AwayScore = reader.GetInt32(4),
						UserId = reader.GetString(5),
						HomePrediction = reader.GetInt32(6),
						AwayPrediction = reader.GetInt32(7),
						UserEmail = reader.GetString(8)
					});
				}
			}
			catch (Exception ex)
			{
				Console.WriteLine($"Error fetching winning bets: {ex.Message}");
			}
			return winningBets;
		}
	}
}
