import { configureStore } from '@reduxjs/toolkit';

import optionsReducer from './features/options/slice';
import userReducer from './features/user/slice';

export const store = configureStore({
	reducer: {
		user: userReducer,
		options: optionsReducer,
	},
});

export type RootState = ReturnType<typeof store.getState>;

export type AppDispatch = typeof store.dispatch;
