import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';


type UserState = {
	settings: Object
};

const initialState: UserState = {
	settings: {}
};

export const optionsSlice = createSlice({
	name: 'options',
	initialState,
	reducers: {
		setOptions: (state, { payload }: PayloadAction<any>) => {
			state.settings = payload;
		},
	},
});

// Action creators are generated for each case reducer function
export const { setOptions } = optionsSlice.actions;

export default optionsSlice.reducer;
