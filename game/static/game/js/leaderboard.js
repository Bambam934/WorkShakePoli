export const STORAGE_KEY = 'leaderboard';
export const MAX_ENTRIES = 10;

export function saveScore(name, score) {
    const data = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
    data.push({ name, score });
    data.sort((a, b) => b.score - a.score);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data.slice(0, MAX_ENTRIES)));
}

export function getScores() {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
}
