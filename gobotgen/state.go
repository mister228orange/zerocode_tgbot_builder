package gobotgen

import (
	"database/sql"
	"time"

	_ "github.com/mattn/go-sqlite3"
)

type User struct {
	ID        int64
	TgID      int64
	Username  string
	CreatedAt time.Time
}

type State struct {
	ID        int64
	UserID    int64
	NodeID    int
	UpdatedAt time.Time
}

func InitDB(path string) (*sql.DB, error) {
	db, err := sql.Open("sqlite3", path)
	if err != nil {
		return nil, err
	}
	_, err = db.Exec(`
	CREATE TABLE IF NOT EXISTS users (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		tgid INTEGER UNIQUE,
		username TEXT,
		created_at DATETIME DEFAULT CURRENT_TIMESTAMP
	);
	CREATE TABLE IF NOT EXISTS states (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		user_id INTEGER,
		node_id INTEGER,
		updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
		FOREIGN KEY(user_id) REFERENCES users(id)
	);
	`)
	if err != nil {
		return nil, err
	}
	return db, nil
}
