import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import axios from "axios";

const initialState = {
    isLoading: false,
    data: {},
    token: '',
    error: undefined,
}

const authenticateUser = createAsyncThunk('user/authenticateUser', async(userData) => {
    const { uname, passwd } = userData;
    const url = 'localhost:5000/auth_view/login';

    const res = await axios.post(url, userData);

    return await res.data;
})

const userSlice = createSlice({
    name: 'user',
    initialState,
    reducers: {

    },
    extraReducers: (builder) => {
        builder
        .addCase(authenticateUser.pending, (state) => {
            state.isLoading = true;
        })
        .addCase(authenticateUser.fulfilled, (state, action) => {
            state.token = action.payload;
        })
        .addCase(authenticateUser.rejected, (state, action) => {
            state.isLoading = false,
            state.error = action.error.message;
        })
    }
})

export {authenticateUser};
export default userSlice;