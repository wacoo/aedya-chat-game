import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import axios from "axios";

const initialState = {
    isLoading: false,
    data: {},
    chatCount: {},
    evalResult: {},
    updateScoreResult: {},
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
    const res = await axios.put(url, data, {
        headers: { 'Content-Type': 'application/json' },
      });

    return await res.data;
});

const updateEvaluation = createAsyncThunk('games/updateEvaluation', async(data) => {
    const url = 'http://localhost:5000/view/addeval';
    console.log(data);
    const res = await axios.put(url, data, {
        headers: { 'Content-Type': 'application/json' },
      });

    return await res.data;
});

const updateScore = createAsyncThunk('games/updateSchore', async(data) => {
    const url = 'http://localhost:5000/view/addscore';
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
        .addCase(updateEvaluation.pending, (state) => {
            state.isLoading = true;
        })
        .addCase(updateEvaluation.fulfilled, (state, action) => {
            state.evalResult = action.payload;
        })
        .addCase(updateEvaluation.rejected, (state, action) => {
            state.isLoading = false;
            state.error = action.error.message;
        })
        .addCase(updateScore.pending, (state) => {
            state.isLoading = true;
        })
        .addCase(updateScore.fulfilled, (state, action) => {
            state.updateScoreResult = action.payload;
        })
        .addCase(updateScore.rejected, (state, action) => {
            state.isLoading = false;
            state.error = action.error.message;
        })
    }
})

export {newGame, fetchGame, updateChatCount, updateEvaluation, updateScore};
export default gamesSlice.reducer;