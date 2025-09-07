package main

import (
	"log"
	"os"

	"gobotgen"

	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func main() {
	botToken := os.Getenv("TELEGRAM_BOT_TOKEN")
	if botToken == "" {
		log.Fatal("TELEGRAM_BOT_TOKEN env var required")
	}
	bot, err := tgbotapi.NewBotAPI(botToken)
	if err != nil {
		log.Panic(err)
	}
	bot.Debug = true
	log.Printf("Authorized on account %s", bot.Self.UserName)

	db, err := gobotgen.InitDB("state.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	u := tgbotapi.NewUpdate(0)
	u.Timeout = 60
	updates := bot.GetUpdatesChan(u)

	for update := range updates {
		if update.Message != nil && update.Message.IsCommand() {
			if update.Message.Command() == "start" {
				// Here: insert user if not exists, set state, etc.
				// ...
			}
		}
		if update.CallbackQuery != nil {
			// Here: update state for user, etc.
			// ...
		}
	}
}
