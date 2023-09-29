import { configureStore } from '@reduxjs/toolkit';
import userReducer from './user/userSlice';
import chatReducer from './chat/chatSlice';
import gamesReducer from './games/gamesSlice';
const store = configureStore({
    reducer: {
        user: userReducer,
        chat: chatReducer,
        games: gamesReducer,
    }
})

export default store;