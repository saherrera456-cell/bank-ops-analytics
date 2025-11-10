# R/eda.R
# Requisitos: install.packages(c("DBI","RSQLite","dplyr","readr","arrow","ggplot2"))
suppressPackageStartupMessages({
  library(DBI)
  library(RSQLite)
  library(dplyr)
  library(readr)
  library(arrow)
  library(ggplot2)
})

base <- normalizePath(".", winslash = "/")
data_dir <- file.path(base, "data")
processed <- file.path(data_dir, "processed", "transactions_clean.parquet")
sqlite_db <- file.path(data_dir, "bank_ops.sqlite")
reports <- file.path(base, "reports")
if (!dir.exists(reports)) dir.create(reports, recursive = TRUE)

read_data <- function() {
  if (file.exists(sqlite_db)) {
    con <- dbConnect(SQLite(), sqlite_db)
    on.exit(dbDisconnect(con))
    df <- dbReadTable(con, "transactions")
  } else if (file.exists(processed)) {
    df <- arrow::read_parquet(processed)
  } else {
    stop("No data source found. Run the Python ETL first.")
  }
  df$tx_timestamp <- as.POSIXct(df$tx_timestamp, tz = "UTC")
  df$date <- as.Date(df$tx_timestamp)
  df$hour <- as.integer(format(df$tx_timestamp, "%H"))
  df
}

df <- read_data()

# Resumen por día
by_date <- df %>%
  group_by(date) %>%
  summarize(
    total_tx = n(),
    total_amount = sum(amount, na.rm = TRUE),
    approved_tx = sum(status == "APPROVED"),
    decline_rate = mean(status == "DECLINED"),
    avg_ticket = mean(amount, na.rm = TRUE),
    .groups = "drop"
  )

readr::write_csv(by_date, file.path(reports, "r_kpi_by_date.csv"))

# Gráfico 1: volumen diario
p1 <- ggplot(by_date, aes(x = date, y = total_tx)) +
  geom_line() +
  labs(title = "Daily Transactions", x = "Date", y = "Transactions")
ggsave(filename = file.path(reports, "r_daily_tx.png"), plot = p1, width = 8, height = 4, dpi = 120)

# Gráfico 2: importe diario
p2 <- ggplot(by_date, aes(x = date, y = total_amount)) +
  geom_line() +
  labs(title = "Daily Amount", x = "Date", y = "Total Amount")
ggsave(filename = file.path(reports, "r_daily_amount.png"), plot = p2, width = 8, height = 4, dpi = 120)

# Funnel por canal
by_channel <- df %>%
  group_by(channel) %>%
  summarize(
    total_tx = n(),
    approval_rate = mean(status == "APPROVED"),
    decline_rate = mean(status == "DECLINED"),
    .groups = "drop"
  )
readr::write_csv(by_channel, file.path(reports, "r_kpi_by_channel.csv"))
