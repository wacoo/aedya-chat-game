import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import axios from "axios";

const initialState = {
    isLoading: false,
    chatList: {},
    error: undefined,
}

const fetchChats = createAsyncThunk('chat/fetchChats', async (credential) => {
    const url = 'http://localhost:5000/view/';
  
    console.log(credential);
    const res = await axios.get(url, {
      headers: { 'Content-Type': 'application/json' },
      params: credential,
    });
  
    return res.data;
  });

const sendChat = createAsyncThunk('chat/sendChat', async(msgObj) => {
    const url = 'http://localhost:5000/view/send';

    // const res = null;
    // if (token && token.email === credential.email) {
        console.log(msgObj);
        const res = await axios.post(url, msgObj, 
            // {
            //     headers: { 'Content-Type': 'application/json',  Authorization: `Bearer ${token.token}`,},
            // }
      );
    // }

    return await res.data;
})

const chatSlice = createSlice({
    name: 'chat',
    initialState,
    extraReducers: (builder) => {
        builder
        .addCase(fetchChats.pending, (state) => {
            state.isLoading = true;
        })
        .addCase(fetchChats.fulfilled, (state, action) => {
            state.chatList = action.payload;
            state.message = {}
        })
        .addCase(fetchChats.rejected, (state, action) => {
            state.isLoading = false;
            state.error = action.error.message;
        })
        .addCase(sendChat.pending, (state) => {
            state.isLoading = true;
        })
        .addCase(sendChat.fulfilled, (state, action) => {
            state.message = action.payload;
        })
        .addCase(sendChat.rejected, (state, action) => {
            state.isLoading = false;
            state.error = action.error.message;
        })
    }
})

export {fetchChats, sendChat};
export default chatSlice.reducer;