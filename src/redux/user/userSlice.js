import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import axios from "axios";

const initialState = {
    isLoading: false,
    message: {},
    token: null,
    error: undefined,
}

const authenticateUser = createAsyncThunk('user/authenticateUser', async(credential) => {
    const url = 'http://localhost:5000/auth/login';

    // console.log(credential);
    let res = null;
    // const token = localStorage.getItem('token');
    // if (token && token.email === credential.email) {
    //     res = await axios.post(url, {
    //         headers: {
    //             Authorization: `Bearer ${token.token}`,
    //         },
    //     });
    // } else {
    res = await axios.post(url, credential, {
        headers: { 'Content-Type': 'application/json' },
    });
    console.log(credential);
    // }
    console.log(await res.data);
    return await res.data;
})

const registerUser = createAsyncThunk('user/registerUser', async(userData) => {
    const url = 'http://localhost:5000/auth/register';

    console.log(userData);
    const res = await axios.post(url, userData, {
        headers: { 'Content-Type': 'application/json' },
      });

    return await res.data;
})

const userSlice = createSlice({
    name: 'user',
    initialState,
    extraReducers: (builder) => {
        builder
        .addCase(authenticateUser.pending, (state) => {
            state.isLoading = true;
        })
        .addCase(authenticateUser.fulfilled, (state, action) => {
            state.isLoading = false;
            state.error = undefined;
            state.token = action.payload;
            console.log(action.payload)
            localStorage.setItem('token', JSON.stringify(state.token));
            state.message = {}
        })
        .addCase(authenticateUser.rejected, (state, action) => {
            state.isLoading = false;
            state.error = action.error.message;
        })
        .addCase(registerUser.pending, (state) => {
            state.isLoading = true;
        })
        .addCase(registerUser.fulfilled, (state, action) => {
            state.isLoading = false;
            state.error = undefined;
            state.message = action.payload;
            state.token = '';
        })
        .addCase(registerUser.rejected, (state, action) => {
            state.isLoading = false;
            state.error = action.error.message;
        })
    }
})

export {authenticateUser, registerUser};
export default userSlice.reducer;