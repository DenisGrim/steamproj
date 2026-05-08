
reviews <- read.csv("reviews.csv")
# Count frequencies
app_counts <- table(reviews$app_id)

# Sort by frequency (optional, but helpful)
app_counts <- sort(app_counts, decreasing = TRUE)

# Create horizontal bar chart
barplot(app_counts,
        main = "Frequency of App IDs",
        xlab = "Count",
        ylab = "App ID",
        las = 1,
        col = "steelblue",
        horiz = TRUE)  # Makes it horizontal
