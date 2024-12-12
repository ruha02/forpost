import type { PayloadAction } from '@reduxjs/toolkit';
import { createSlice } from '@reduxjs/toolkit';

type UserState = {
	data: Api.Response.UserRead | null;
	// data: Api.Response.User | null;
};

const initialState: UserState = {
	data: null,
};

export const userSlice = createSlice({
	name: 'user',
	initialState,
	reducers: {
		setUser: (state, { payload }: PayloadAction<Api.Response.UserRead>) => {
			state.data = payload;
		},
	},
});

// Action creators are generated for each case reducer function
export const { setUser } = userSlice.actions;

export default userSlice.reducer;
