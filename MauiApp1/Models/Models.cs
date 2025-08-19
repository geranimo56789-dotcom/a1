using Newtonsoft.Json;

namespace MauiApp1.Models
{
    public class Match
    {
        [JsonProperty("matchId")]
        public required string MatchId { get; set; }

        [JsonProperty("homeTeam")]
        public required string HomeTeam { get; set; }

        [JsonProperty("awayTeam")]
        public required string AwayTeam { get; set; }

        [JsonProperty("homeTeamCode")]
        public required string HomeTeamCode { get; set; }

        [JsonProperty("awayTeamCode")]
        public required string AwayTeamCode { get; set; }

        [JsonProperty("league")]
        public required string League { get; set; }

        [JsonProperty("timeUtc")]
        public long TimeUtc { get; set; }

        [JsonProperty("time")]
        public required string Time { get; set; }

        [JsonProperty("homeScore")]
        public int? HomeScore { get; set; }

        [JsonProperty("awayScore")]
        public int? AwayScore { get; set; }
    }

    public class Prediction
    {
        [JsonProperty("matchId")]
        public required string MatchId { get; set; }

        [JsonProperty("homeScore")]
        public int HomeScore { get; set; }

        [JsonProperty("awayScore")]
        public int AwayScore { get; set; }

        [JsonProperty("homeTeam")]
        public required string HomeTeam { get; set; }

        [JsonProperty("awayTeam")]
        public required string AwayTeam { get; set; }

        [JsonProperty("homeTeamCode")]
        public required string HomeTeamCode { get; set; }

        [JsonProperty("awayTeamCode")]
        public required string AwayTeamCode { get; set; }

        [JsonProperty("createdAt")]
        public long CreatedAt { get; set; }

        [JsonProperty("lockAt")]
        public long LockAt { get; set; }
    }

    public class User
    {
        public string Email { get; set; } = "";
        public string Uid { get; set; } = "";
        public bool IsAdmin => Email.ToLower() == "admin@gmail.com";
    }

    public class TeamInfo
    {
        public string Code { get; set; } = "";
        public string Name { get; set; } = "";
        public Color Color { get; set; } = Colors.Blue;
    }

    public class WinningBet
    {
        public string MatchId { get; set; } = "";
        public string HomeTeam { get; set; } = "";
        public string AwayTeam { get; set; } = "";
        public int HomeScore { get; set; }
        public int AwayScore { get; set; }
        public string UserId { get; set; } = "";
        public int HomePrediction { get; set; }
        public int AwayPrediction { get; set; }
        public string UserEmail { get; set; } = "";
    }
}
