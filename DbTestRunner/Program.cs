using Npgsql;
using System;
using System.Threading.Tasks;

class Program
{
    static async Task Main()
    {
        var connString = "Host=db.nheuamtrbsogjeuibqtf.supabase.co;Port=5432;Username=postgres;Password=yahoome1;Database=postgres;Sslmode=Require;";

        try
        {
            await using var conn = new NpgsqlConnection(connString);
            await conn.OpenAsync();
            Console.WriteLine("✅ Connected to Supabase Postgres");

            // Ensure schema for Matches
            const string createMatches = @"CREATE TABLE IF NOT EXISTS public.""Matches"" (
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
            await using (var cmd = new NpgsqlCommand(createMatches, conn))
                await cmd.ExecuteNonQueryAsync();

            // Ensure schema for Predictions
            const string createPredictions = @"CREATE TABLE IF NOT EXISTS public.""Predictions"" (
                ""UserId"" text NOT NULL,
                ""MatchId"" text NOT NULL,
                ""HomePrediction"" integer NOT NULL,
                ""AwayPrediction"" integer NOT NULL,
                ""CreatedAt"" bigint NOT NULL,
                ""LockAt"" bigint NOT NULL,
                PRIMARY KEY (""UserId"", ""MatchId"")
            );";
            await using (var cmd = new NpgsqlCommand(createPredictions, conn))
                await cmd.ExecuteNonQueryAsync();

            // Seed two matches idempotently
            var now = DateTimeOffset.UtcNow;
            var m1Id = "seed-ARS-CHE";
            var m2Id = "seed-LIV-MCI";

            const string upsertMatch = @"INSERT INTO public.""Matches"" (""MatchId"", ""HomeTeam"", ""AwayTeam"", ""HomeTeamCode"", ""AwayTeamCode"", ""League"", ""TimeUtc"", ""Time"", ""HomeScore"", ""AwayScore"")
                VALUES (@MatchId, @HomeTeam, @AwayTeam, @HomeTeamCode, @AwayTeamCode, @League, @TimeUtc, @Time, NULL, NULL)
                ON CONFLICT (""MatchId"") DO NOTHING;";

            await using (var up1 = new NpgsqlCommand(upsertMatch, conn))
            {
                up1.Parameters.AddWithValue("@MatchId", m1Id);
                up1.Parameters.AddWithValue("@HomeTeam", "Arsenal");
                up1.Parameters.AddWithValue("@AwayTeam", "Chelsea");
                up1.Parameters.AddWithValue("@HomeTeamCode", "ARS");
                up1.Parameters.AddWithValue("@AwayTeamCode", "CHE");
                up1.Parameters.AddWithValue("@League", "VAR6");
                up1.Parameters.AddWithValue("@TimeUtc", now.AddHours(2).ToUnixTimeSeconds());
                up1.Parameters.AddWithValue("@Time", "15:00");
                await up1.ExecuteNonQueryAsync();
            }

            await using (var up2 = new NpgsqlCommand(upsertMatch, conn))
            {
                up2.Parameters.AddWithValue("@MatchId", m2Id);
                up2.Parameters.AddWithValue("@HomeTeam", "Liverpool");
                up2.Parameters.AddWithValue("@AwayTeam", "Manchester City");
                up2.Parameters.AddWithValue("@HomeTeamCode", "LIV");
                up2.Parameters.AddWithValue("@AwayTeamCode", "MCI");
                up2.Parameters.AddWithValue("@League", "VAR6");
                up2.Parameters.AddWithValue("@TimeUtc", now.AddHours(4).ToUnixTimeSeconds());
                up2.Parameters.AddWithValue("@Time", "17:30");
                await up2.ExecuteNonQueryAsync();
            }

            // Verify matches
            const string countSql = "SELECT COUNT(*) FROM public.\"Matches\"";
            await using var countCmd = new NpgsqlCommand(countSql, conn);
            var total = (long)(await countCmd.ExecuteScalarAsync() ?? 0L);
            Console.WriteLine($"Total matches in DB: {total}");

            const string listSql = "SELECT \"MatchId\", \"HomeTeam\", \"AwayTeam\", \"Time\" FROM public.\"Matches\" ORDER BY \"TimeUtc\" LIMIT 5";
            await using var listCmd = new NpgsqlCommand(listSql, conn);
            await using var reader = await listCmd.ExecuteReaderAsync();
            while (await reader.ReadAsync())
            {
                Console.WriteLine($" - {reader.GetString(0)}: {reader.GetString(1)} vs {reader.GetString(2)} at {reader.GetString(3)}");
            }
            await reader.DisposeAsync();

            // Seed predictions for a test user
            var userId = "test_user";
            const string upsertPred = @"INSERT INTO public.""Predictions"" (""UserId"", ""MatchId"", ""HomePrediction"", ""AwayPrediction"", ""CreatedAt"", ""LockAt"")
                VALUES (@UserId, @MatchId, @HomePrediction, @AwayPrediction, @CreatedAt, @LockAt)
                ON CONFLICT (""UserId"", ""MatchId"") DO UPDATE SET
                    ""HomePrediction"" = EXCLUDED.""HomePrediction"",
                    ""AwayPrediction"" = EXCLUDED.""AwayPrediction"",
                    ""CreatedAt"" = EXCLUDED.""CreatedAt"";";

            await using (var pp1 = new NpgsqlCommand(upsertPred, conn))
            {
                pp1.Parameters.AddWithValue("@UserId", userId);
                pp1.Parameters.AddWithValue("@MatchId", m1Id);
                pp1.Parameters.AddWithValue("@HomePrediction", 2);
                pp1.Parameters.AddWithValue("@AwayPrediction", 1);
                pp1.Parameters.AddWithValue("@CreatedAt", DateTimeOffset.UtcNow.ToUnixTimeSeconds());
                pp1.Parameters.AddWithValue("@LockAt", now.AddHours(2).ToUnixTimeSeconds());
                await pp1.ExecuteNonQueryAsync();
            }

            await using (var pp2 = new NpgsqlCommand(upsertPred, conn))
            {
                pp2.Parameters.AddWithValue("@UserId", userId);
                pp2.Parameters.AddWithValue("@MatchId", m2Id);
                pp2.Parameters.AddWithValue("@HomePrediction", 1);
                pp2.Parameters.AddWithValue("@AwayPrediction", 1);
                pp2.Parameters.AddWithValue("@CreatedAt", DateTimeOffset.UtcNow.ToUnixTimeSeconds());
                pp2.Parameters.AddWithValue("@LockAt", now.AddHours(4).ToUnixTimeSeconds());
                await pp2.ExecuteNonQueryAsync();
            }

            // Verify predictions
            const string predCountSql = "SELECT COUNT(*) FROM public.\"Predictions\" WHERE \"UserId\"=@UserId";
            await using var pc = new NpgsqlCommand(predCountSql, conn);
            pc.Parameters.AddWithValue("@UserId", userId);
            var pcount = (long)(await pc.ExecuteScalarAsync() ?? 0L);
            Console.WriteLine($"Total predictions for {userId}: {pcount}");

            const string predJoinSql = @"SELECT p.""MatchId"", p.""HomePrediction"", p.""AwayPrediction"", m.""HomeTeam"", m.""AwayTeam""
                FROM public.""Predictions"" p JOIN public.""Matches"" m ON m.""MatchId""=p.""MatchId"" WHERE p.""UserId""=@UserId ORDER BY m.""TimeUtc""";
            await using var pj = new NpgsqlCommand(predJoinSql, conn);
            pj.Parameters.AddWithValue("@UserId", userId);
            await using var r2 = await pj.ExecuteReaderAsync();
            while (await r2.ReadAsync())
            {
                Console.WriteLine($" * {r2.GetString(3)} vs {r2.GetString(4)} => {r2.GetInt32(1)}-{r2.GetInt32(2)}");
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"❌ Seeding or verification failed: {ex.Message}");
            Environment.ExitCode = 1;
        }
    }
}
