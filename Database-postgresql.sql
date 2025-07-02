-- Удаление старых таблиц (опционально)
DROP TABLE IF EXISTS public.games;
DROP TABLE IF EXISTS public.players;

-- Таблица пользователей
CREATE TABLE public.players (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(30) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    CONSTRAINT username_length_check CHECK (username <> '')
);

-- Таблица игр
CREATE TABLE public.games (
    game_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    number_of_guesses INTEGER NOT NULL,
    secret_number INTEGER NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    CONSTRAINT games_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.players (user_id) ON DELETE CASCADE,
    CONSTRAINT number_of_guesses_positive CHECK (number_of_guesses > 0),
    CONSTRAINT secret_number_range CHECK (secret_number BETWEEN 1 AND 1000)
);

-- Индексы
CREATE INDEX idx_games_user_id ON public.games(user_id);
CREATE INDEX idx_games_created_at ON public.games(created_at);

-- Комментарии
COMMENT ON TABLE public.players IS 'Пользователи игры "Угадай число"';
COMMENT ON TABLE public.games IS 'Игры пользователей';
COMMENT ON COLUMN public.games.secret_number IS 'Загаданное число (от 1 до 1000)';
COMMENT ON COLUMN public.games.number_of_guesses IS 'Количество попыток для угадывания';
