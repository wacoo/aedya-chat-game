import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import axios from "axios";

const initialState = {
    isLoading: false,
    data: {},
    chatCount: {},
    error: undefined,
}

const newGame = createAsyncThunk('games/newGame', async(data) => {
    const url = 'http://localhost:5000/view/newgame';
    // console.log(data);
    const res = await axios.post(url, data, {
        headers: { 'Content-Type': 'application/json' },
      });

    return await res.data;
});

const fetchGame = createAsyncThunk('games/getgame', async(data) => {
    const url = 'http://localhost:5000/view/getgame';
    console.log(data);
    const res = await axios.get(url, {
        headers: { 'Content-Type': 'application/json' },
        params: data,
      });

    return await res.data;
});
const updateChatCount = createAsyncThunk('games/updateChatCount', async(data) => {
    const url = 'http://localhost:5000/view/updatecount';
    console.log(data);
    const res = await axios.put(url, data, {
        headers: { 'Content-Type': 'application/json' },
      });

    return await res.data;
});
const gamesSlice = createSlice({
    name: 'games',
    initialState,
    extraReducers: (builder) => {
        builder
        .addCase(newGame.pending, (state) => {
            state.isLoading = true;
        })
        .addCase(newGame.fulfilled, (state, action) => {
            state.data = action.payload;
        })
        .addCase(newGame.rejected, (state, action) => {
            state.isLoading = false;
            state.error = action.error.message;
        })
        .addCase(fetchGame.pending, (state) => {
            state.isLoading = true;
        })
        .addCase(fetchGame.fulfilled, (state, action) => {
            state.data = action.payload;
        })
        .addCase(fetchGame.rejected, (state, action) => {
            state.isLoading = false;
            state.error = action.error.message;
        })
        .addCase(updateChatCount.pending, (state) => {
            state.isLoading = true;
        })
        .addCase(updateChatCount.fulfilled, (state, action) => {
            state.chatCount = action.payload;
        })
        .addCase(updateChatCount.rejected, (state, action) => {
            state.isLoading = false;
            state.error = action.error.message;
        })
    }
})

export {newGame, fetchGame, updateChatCount};
export default gamesSlice.reducer;