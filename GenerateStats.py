# My Modules
from MyModules.NFLStats import GenerateTeamStatsCSV, GenerateSeasonStatsCSV, GenerateStatsMetricsCSV

# Third Party Modules
from sys import argv, exit

# Error handler
try:
    if (not str.isnumeric(argv[1])):
        exit("INVALID COMMAND ARGUMENT: First argument MUST be a numerical value!")

except IndexError:
    exit("NO ARGUMENTS FOUND: Please enter a year as an argument!")

year = argv[1]

# Generate Team Stats
GenerateTeamStatsCSV(year)

# Generate Season Stats
GenerateSeasonStatsCSV(year)

# Generate Stats Metrics
GenerateStatsMetricsCSV(year)