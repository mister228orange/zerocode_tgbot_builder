package main

import (
	log "log"
	os "os"
	strconv "strconv"

	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

// Node represents a node in the decision tree
type Node struct {
	ID       int
	Value    string
	IsLeaf   bool
	Children []int // IDs of child nodes
}

// Edge represents an edge in the decision tree
type Edge struct {
	Source int
	Target int
	Label  string
}

// Graph holds the nodes and edges
type Graph struct {
	Nodes map[int]*Node
	Edges []Edge
}

// Example: hardcoded graph, replace with XML parsing logic
type UserState struct {
	CurrentNode int
}

var (
	graph = Graph{
		Nodes: map[int]*Node{
			0: {ID: 0, Value: "Lamp doesn't work", IsLeaf: false, Children: []int{1}},
			1: {ID: 1, Value: "Lamp plugged in?", IsLeaf: false, Children: []int{2, 3}},
			2: {ID: 2, Value: "Plug in lamp", IsLeaf: true, Children: nil},
			3: {ID: 3, Value: "Bulb burned out?", IsLeaf: false, Children: []int{4, 5}},
			4: {ID: 4, Value: "Replace Bulb", IsLeaf: true, Children: nil},
			5: {ID: 5, Value: "Repair Lamp", IsLeaf: true, Children: nil},
		},
		Edges: []Edge{
			{Source: 0, Target: 1, Label: ""},
			{Source: 1, Target: 2, Label: "No"},
			{Source: 1, Target: 3, Label: "Yes"},
			{Source: 3, Target: 4, Label: "Yes"},
			{Source: 3, Target: 5, Label: "No"},
		},
	}
	userStates = map[int64]*UserState{}
)

func getChildren(nodeID int) []Edge {
	var children []Edge
	for _, e := range graph.Edges {
		if e.Source == nodeID {
			children = append(children, e)
		}
	}
	return children
}

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

	u := tgbotapi.NewUpdate(0)
	u.Timeout = 60
	updates := bot.GetUpdatesChan(u)

	for update := range updates {
		if update.Message != nil && update.Message.IsCommand() {
			if update.Message.Command() == "start" {
				userStates[update.Message.Chat.ID] = &UserState{CurrentNode: 0}
				sendNode(bot, update.Message.Chat.ID, 0)
			}
		}
		if update.CallbackQuery != nil {
			userID := update.CallbackQuery.Message.Chat.ID
			choice, _ := strconv.Atoi(update.CallbackQuery.Data)
			userStates[userID].CurrentNode = choice
			sendNode(bot, userID, choice)
			bot.AnswerCallbackQuery(tgbotapi.NewCallback(update.CallbackQuery.ID, ""))
		}
	}
}

func sendNode(bot *tgbotapi.BotAPI, chatID int64, nodeID int) {
	node := graph.Nodes[nodeID]
	if node.IsLeaf {
		msg := tgbotapi.NewMessage(chatID, node.Value+"\n(leaf node)")
		bot.Send(msg)
		return
	}
	children := getChildren(nodeID)
	var buttons [][]tgbotapi.InlineKeyboardButton
	for _, e := range children {
		child := graph.Nodes[e.Target]
		label := e.Label
		if label == "" {
			label = child.Value
		}
		buttons = append(buttons, tgbotapi.NewInlineKeyboardRow(
			tgbotapi.NewInlineKeyboardButtonData(label, strconv.Itoa(child.ID)),
		))
	}
	msg := tgbotapi.NewMessage(chatID, node.Value)
	msg.ReplyMarkup = tgbotapi.NewInlineKeyboardMarkup(buttons...)
	bot.Send(msg)
}
