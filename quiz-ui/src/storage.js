export default {
    clear() {
        window.localStorage.removeItem("playerName");
    },
    savePlayerName(playerName) {
        window.localStorage.setItem("playerName", playerName);
    },
    getPlayerName() {
        return window.localStorage.getItem("playerName");
    },
    saveParticipationScore(participationScore) {
        window.localStorage.setItem("participationScore", participationScore);
    },
    getParticipationScore() {
        return window.localStorage.getItem("participationScore");
    },
    saveAdminToken(token) {
        window.localStorage.setItem("adminToken", token);
    },
    getAdminToken(token) {
        return window.localStorage.getItem("adminToken", token);
    }
};