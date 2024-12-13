import { useEffect, useState } from 'react';
import { Navigate, createBrowserRouter, useNavigate } from 'react-router-dom';
import { SpinLoader } from './components/SpinLoader';
import { useAppSelector } from './hooks/useAppSelector';
import Main from './Main';
import { InfoSystem } from './pages/InfoSystem';
import { Login } from './pages/Login';
import { Question } from './pages/Question';
import { Source } from './pages/Source';
import { User } from './pages/User';

const ProtectedRoute = ({ children, is_superuser }: { children: any; is_superuser: boolean }) => {
	const user: Api.Response.UserRead = useAppSelector((state: any) => state.user.data)
	const nav = useNavigate()
	const [data, setData] = useState(<SpinLoader />)

	useEffect(() => {

		if (user) {
			setData(children)
		} else {
			nav('/')
		}
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [])
	return data
}


export const router = createBrowserRouter([
	{
		path: '/',
		element: <Main />,
		children: [
			{
				path: '/info_system',
				element: (
					<ProtectedRoute is_superuser={false}>
						<InfoSystem />
					</ProtectedRoute>
				),
			},

			{
				path: '/user',
				element: (
					<ProtectedRoute is_superuser={true}>
						<User />
					</ProtectedRoute>
				),
			},
			{
				path: '/source',
				element: (
					<ProtectedRoute is_superuser={true}>
						<Source />
					</ProtectedRoute>
				),
			},
			{
				path: '/question',
				element: (
					<ProtectedRoute is_superuser={true}>
						<Question />
					</ProtectedRoute>
				),
			},
		],
	},
	{
		path: '/login',
		element: <Login />,
	},
	{
		path: '*',
		element: <Navigate to='/info_system' />,
	},
], {
	future: {
		v7_fetcherPersist: true,
		v7_normalizeFormMethod: true,
		v7_partialHydration: true,
		v7_relativeSplatPath: true,
		v7_skipActionErrorRevalidation: true,
	}
});